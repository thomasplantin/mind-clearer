db = db.getSiblingDB("mind_clearer_db");
db.users_tb.drop();

db.users_tb.insertMany([
    {
        "id": 1,
        "username": "thomas@email.com",
        "thoughts": "thought 1"
    },
    {
        "id": 2,
        "username": "kyle@email.com",
        "thoughts": "thought 2"
    }
]);