
## Assignment 6 -  Restaurants DB (with MongoDB)

### Byron Dowling

#### Description

> - Api will run on port 8003 on this server **<http://143.244.188.178/:8003>**
> - Loaded the restaurant DataBase **([restaurant.json](restaurant.json))** on my server using MongoDB.
> - Any Data returned by a route will be paginated with a preset page size.
> - Created indexes for certain queries that allow the runtime to be faster also allow certain data to be processed.
>
> - **Routes:**
>   - Restaurants
>     - All restaurants (paginated result).
>     - Unique restaurant categories.
>     - All restaurants in a category.
>     - All restaurants in a list of 1 or more zip codes.
>     - All restaurants near Point(x,y).
>     - All restaurants with a min rating of X.
>

### Files

|   #   | File                               | Description          | Status                  |
| :---: | ---------------------------------- | -------------------- | ----------------------- |
|   1   | [main.py](main.py)                 | Main code            | :ballot_box_with_check: |


### References

|   #   | Files                                                                                                                                                                                                                                                | Description               | Status                  |
| :---: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | ----------------------- |
|   1   | [https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04)                                                                   | Install MongoDB           | :ballot_box_with_check: |
|   2   | [https://www.digitalocean.com/community/tutorials/how-to-configure-remote-access-for-mongodb-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-configure-remote-access-for-mongodb-on-ubuntu-20-04)                           | Remote Access for MongoDB | :ballot_box_with_check: |
|   3   | [https://www.digitalocean.com/community/tutorials/how-to-perform-crud-operations-in-mongodb-using-pymongo-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-perform-crud-operations-in-mongodb-using-pymongo-on-ubuntu-20-04) | Py Mongo                  | :ballot_box_with_check: |
|   4   | [https://docs.mongodb.com/mongodb-shell/crud/read/#std-label-mongosh-read](https://docs.mongodb.com/mongodb-shell/crud/read/#std-label-mongosh-read)                                                                                                 | Query Documents           | :ballot_box_with_check: |
