// PART 1 - MongoDB

// 1.1 Create db

use tech_blog_db

const itRoles = [
    'Frontend Developer', 
    'Backend Developer', 
    'DevOps Engineer', 
    'Software Engineer', 
    'Data Engineer', 
    'QA Engineer', 
    'Full Stack Developer'
];

const seniorities = ['Junior', 'Mid', 'Senior', 'Lead', 'Principal'];

const categories = [
    'JavaScript', 'Python', 'Java', 'DevOps', 
    'Cloud', 'Architecture', 'Best Practices', 
    'Testing', 'Security', 'Machine Learning', `Database`
];

const postTitles = [
    'Introduction to', 'Advanced', 'Best practices in', 
    'How to implement', 'Understanding', 'Deep dive into',
    'Tutorial:', 'Guide to', 'Mastering'
];

db.createCollection("users", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["name", "email", "it_role", "seniority"],
            properties: {
                name: {
                    bsonType: "string",
                    minLength: 2,
                    maxLength: 50
                },
                email: {
                    bsonType: "string",
                    pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                },
                it_role: {
                    enum: itRoles
                },
                seniority: {
                    enum: seniorities
                },
                join_date: {
                    bsonType: "date"
                },
                bio: {
                    bsonType: "string",
                    maxLength: 500
                }
            }
        }
    }
})

db.createCollection("posts", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["title", "author_id", "content", "category", "date"],
            properties: {
                title: {
                    bsonType: "string",
                    minLength: 5,
                    maxLength: 200
                },
                author_id: {
                    bsonType: "objectId"
                },
                content: {
                    bsonType: "string",
                    minLength: 20
                },
                category: {
                    enum: categories
                },
                date: {
                    bsonType: "date"
                },
                likes: {
                    bsonType: "int",
                    minimum: 0
                },
                tags: {
                    bsonType: "array",
                    items: {
                        bsonType: "string"
                    }
                }
            }
        }
    }
})

db.createCollection("comments", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["post_id", "user_id", "content", "date"],
            properties: {
                post_id: {
                    bsonType: "objectId"
                },
                user_id: {
                    bsonType: "objectId"
                },
                content: {
                    bsonType: "string",
                    minLength: 0,
                    maxLength: 200
                },
                date: {
                    bsonType: "date"
                },
                likes: {
                    bsonType: "int",
                    minimum: 0
                }
            }
        }
    }
})



// 1.2 Create helper functions

function randomInt(min, max) {
    return NumberInt(Math.floor(Math.random() * (max - min + 1)) + min);
}

function randomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
}

function randomElement(array) {
    return array[Math.floor(Math.random() * array.length)];
}

const itRoles = [
    'Frontend Developer', 
    'Backend Developer', 
    'DevOps Engineer', 
    'Software Engineer', 
    'Data Engineer', 
    'QA Engineer', 
    'Full Stack Developer'
];

const seniorities = ['Junior', 'Mid', 'Senior', 'Lead', 'Principal'];

const categories = [
    'JavaScript', 'Python', 'Java', 'DevOps', 
    'Cloud', 'Architecture', 'Best Practices', 
    'Testing', 'Security', 'Machine Learning', `Database`
];

const postTitles = [
    'Introduction to', 'Advanced', 'Best practices in', 
    'How to implement', 'Understanding', 'Deep dive into',
    'Tutorial:', 'Guide to', 'Mastering'
];



// 1.3 Generate random data

function generateUsers(count) {
    let users = [];
    for (let i = 0; i < count; i++) {
	    const seniorityLevel = randomElement(seniorities);
        const role = randomElement(itRoles);
        
        users.push({
            name: `User${i}`,
            email: `user${i}@techblog.com`,
            it_role: role,
            seniority: seniorityLevel,
            join_date: randomDate(new Date(2020, 0, 1), new Date()),
            bio: `Experienced ${seniorityLevel} ${role}`
        });
    }
    return users;
}

function generatePosts(userIds, count) {
    let posts = [];
    for (let i = 0; i < count; i++) {
	    const postCategory = randomElement(categories)
	    
        posts.push({
            title: `${randomElement(postTitles)} ${postCategory}`,
            author_id: randomElement(userIds),
            content: `This is a detailed post about ${postCategory}. Content number ${i}`,
            category: postCategory,
            date: randomDate(new Date(2020, 0, 1), new Date()),
            likes: randomInt(0, 200)
        });
    }
    return posts;
}

function generateComments(postIds, userIds, count) {
    let comments = [];
    for (let i = 0; i < count; i++) {
        comments.push({
            post_id: randomElement(postIds),
            user_id: randomElement(userIds),
            content: `This is comment number ${i}`,
            date: randomDate(new Date(2020, 0, 1), new Date()),
            likes: randomInt(0, 50)
        });
    }
    return comments;
}

console.log("Inserting users...");
let users = generateUsers(1000);
let userInsertResult = db.users.insertMany(users);

console.log("Inserting posts...");
let userIds = db.users.distinct('_id');
let posts = generatePosts(userIds, 5000);
let postInsertResult = db.posts.insertMany(posts);

console.log("Inserting comments...");
let postIds = db.posts.distinct('_id');

let comments = generateComments(postIds, userIds, 10000);
db.comments.insertMany(comments);

console.log("Data generation completed.");



// 1.4 setup basic CRUD operations

let authorId = db.users.distinct('_id')[0];

db.posts.insertOne({
    title: "New Post About MongoDB",
    author_id: authorId,
    content: "This is a new post about MongoDB...",
    category: "Database",
    date: new Date(),
    likes: 0,
    tags: ["MongoDB", "Database"]
});

db.posts.findOne({ title: "New Post About MongoDB" });

db.posts.find({ category: "JavaScript" });
db.posts.find({ likes: { $gt: 50 } });

db.posts.updateOne(
    { title: "New Post About MongoDB" },
    { 
        $set: { 
            title: "Updated Title",
            content: "Updated content of the manually added post"
        },
        $inc: { likes: 1 }
    }
);

db.posts.updateMany(
    { category: "Database" },
    { $inc: { likes: 10 } }
);

db.posts.deleteOne({ title: "Updated Title" });



// 1.5 create aggregation pipelines (advanced operations)

db.posts.aggregate([
    {
        $lookup: {
            from: "users",
            localField: "author_id",
            foreignField: "_id",
            as: "author"
        }
    },
    { $unwind: "$author" },
    {
        $group: {
            _id: "$author.it_role",
            total_posts: { $sum: 1 },
            total_likes: { $sum: "$likes" },
            avg_likes: { $avg: "$likes" }
        }
    },
    { $sort: { total_posts: -1 } }
]);

db.posts.aggregate([
  {
    $group: {
      _id: "$category",
      totalLikes: { $sum: "$likes" },
      postCount: { $sum: 1 }
    }
  },
  { $sort: { totalLikes: -1 } },
  {
    $project: {
      _id: 0,
      category: "$_id",
      totalLikes: 1,
      postCount: 1
    }
  }
]);

db.posts.aggregate([
    {
        $lookup: {
            from: "comments",
            localField: "_id",
            foreignField: "post_id",
            as: "post_comments"
        }
    },
    {
        $project: {
            title: 1,
            comment_count: { $size: "$post_comments" },
            total_comment_likes: { $sum: "$post_comments.likes" }
        }
    },
    { $sort: { comment_count: -1 } },
    { $limit: 10 }
]);



// 1.6 Create indexes

db.posts.createIndex({ category: 1 });

db.posts.find({ category: "Cloud" }).explain("executionStats");

db.users.createIndex({ it_role: 1, seniority: 1 });