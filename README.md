# serviceITnow
A web application that allows the user to create "feature requests".

User Website: http://radhey0105.pythonanywhere.com/

Go to above URL and enter username and password. (login credentials will be shared seperately.)

Admin Portal: http://radhey0105.pythonanywhere.com/admin/

Go to above URL and enter username and password. (login credentials will be shared seperately.)



A "feature request" is a request for a new feature that will be added onto an existing
piece of software. Assume that the user is an employee who would be
entering this information after having some correspondence with the client that is
requesting the feature.

Below are the Fields of a "feature request":

  1. Title: A short, descriptive name of the feature request.
  2. Description: A long description of the feature request.
  3. Client: A selection list of clients (like "Client A", "Client B", "Client C")
  4. Client Priority: Client Priority numbers will not be repeated for the given client.
  so if a priority is set on a new feature as "1", then all other feature requests for that client should be reordered. 
  Priority 0 means no priority is set yet.
  5. Target Date: The date that the client is hoping to have the feature.
  6. Product Area: A selection list of product areas (like 'Policies', 'Billing', 'Claims', 'Reports')
  7. Status: Current status of the request.

DB Schemas:
  1. features: Stores feature requests. Have Many to one relationship with "clients" and "productarea"
  2. clients: Stores client's information.
  3. productarea: Stores product area information.
  4. Django's default auth models are being used.

Priority reordering:
  1. Overriding save method of model to address priority reordering.
  2. Only Feature request that have status=A will be priorities.
  3. Priority 0 means the item is not priorities yet. If an item has status=A and priority=0
     then it will not be reordered automatically.
  4. Priority will be always sequential i. e. If priority 1,2,3 is already assigned and new item is added with
     priority 5 then is will be assigned priority 4.
  5. If a priority is set on a new feature as "1", then all other feature requests for that client that have
     status=A will be reordered.
  6. This methods hits DB only once for reordering multiple features.
  
Note:
  1. Clients, Product Areas and users can be added via admin portal.
  2. Feature Request can be also added via admin portal.
  3. Paging is implemented on home page, 10 reature request will be displayed on one page.
  

