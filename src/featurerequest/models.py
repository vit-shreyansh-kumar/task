from django.db import models
from django.db.models import Max, F
from django.core.validators import MinValueValidator


class Clients(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    startdate = models.DateTimeField(auto_now_add=True)
    enddate = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    class Meta:
        verbose_name_plural = "clients"

    def __str__(self):
        return self.name


class ProductArea(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class Features(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('D', 'Done'),
        ('C', 'Cancelled'),
    )

    PRIORITY_CHOICES = tuple((i, i) for i in range(0, 16))

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=8000)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # 0 means priority is not set
    start_date = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField()
    product_area = models.ForeignKey(ProductArea,  null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name_plural = "features"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        1. Overriding save method to address priority reordering.
        2. Only Feature request that have status=A will be priorities.
        3. Priority 0 means the item is not priorities yet. If an item has status=A and priority=0
           then it will not be reordered automatically.
        4. Priority will be always sequential i. e. If priority 1,2,3 is already assigned and new item is added with
           priority 5 then is will be assigned priority 4.
        5. If a priority is set on a new feature as "1", then all other feature requests for that client that have
           status=A will be reordered.
        6. This methods hits DB only once for reordering multiple features.

        """
        if not self.pk:  # inserting new feature request
            if self.status == 'A':
                    max_priority = Features.objects.filter(client=self.client, status='A').aggregate(
                        Max('priority'))['priority__max']
                    if self.priority ==0:
                        pass
                    elif max_priority is not None and self.priority > max_priority:
                        self.priority = max_priority + 1
                    else:
                        Features.objects.filter(client=self.client, priority__gte=self.priority,
                                                ).exclude(priority=0).update(priority=F('priority') + 1)
            else:
                self.priority = 0
        else:  # updating feature request
            old_feature_object = Features.objects.get(pk=self.pk)
            old_priority = old_feature_object.priority
            old_status = old_feature_object.status
            self.client = old_feature_object.client  # client can not be modified
            new_priority = self.priority
            new_status = self.status
            if new_priority == old_priority and new_status == old_status:
                pass  # no reordering required
            else:
                if new_status == 'A':
                    if old_priority == 0:
                        Features.objects.filter(client=self.client, priority__gte=new_priority,
                                                ).exclude(priority=0).update(priority=F('priority') + 1)
                    elif new_priority == 0:
                        Features.objects.filter(client=self.client, priority__gte=old_priority,
                                                ).exclude(priority=0).update(priority=F('priority') - 1)
                    elif new_priority > old_priority:
                        Features.objects.filter(client=self.client, priority__gt=old_priority, priority__lte=new_priority,
                                                ).exclude(priority=0).update(priority=F('priority') - 1)
                    else:
                        Features.objects.filter(client=self.client, priority__gte=new_priority, priority__lt=old_priority,
                                                ).exclude(priority=0).update(priority=F('priority') + 1)

                    max_priority = Features.objects.filter(client=self.client, status='A').aggregate(
                        Max('priority'))['priority__max']

                    if max_priority is not None and new_priority > max_priority:
                        self.priority = max_priority + 1  # priority must be sequential
                else:
                    self.priority = 0  # only features that have status=A can be priorities
        super().save(*args, **kwargs)  # calling super to do the default action.

