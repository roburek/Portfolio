aws dynamodb put-item \
    --table-name MediaProducts-mateusz-skrobek \
    --item '{
        "product_id": {"S": "BOOK001"},
        "category": {"S": "książka"},
        "title": {"S": "Władca Pierścieni"},
        "author_artist": {"S": "J.R.R. Tolkien"},
        "release_year": {"N": "1954"},
        "price": {"N": "49.99"},
        "genre": {"S": "fantasy"},
        "language": {"S": "polski"},
        "rating": {"N": "5"}
    }'

aws dynamodb put-item \
    --table-name MediaProducts-mateusz-skrobek \
    --item '{
        "product_id": {"S": "MUSIC001"},
        "category": {"S": "muzyka"},
        "title": {"S": "The Dark Side of the Moon"},
        "author_artist": {"S": "Pink Floyd"},
        "release_year": {"N": "1973"},
        "price": {"N": "29.99"},
        "genre": {"S": "rock"},
        "language": {"S": "angielski"},
        "rating": {"N": "5"}
    }'

aws dynamodb put-item \
    --table-name MediaProducts-mateusz-skrobek \
    --item '{
        "product_id": {"S": "MOVIE001"},
        "category": {"S": "film"},
        "title": {"S": "Inception"},
        "author_artist": {"S": "Christopher Nolan"},
        "release_year": {"N": "2010"},
        "price": {"N": "34.99"},
        "genre": {"S": "sci-fi"},
        "language": {"S": "polski/angielski"},
        "rating": {"N": "4"}
    }'

aws dynamodb put-item \
    --table-name MediaProducts-mateusz-skrobek \
    --item '{
        "product_id": {"S": "GAME001"},
        "category": {"S": "gra"},
        "title": {"S": "The Witcher 3"},
        "author_artist": {"S": "CD Projekt Red"},
        "release_year": {"N": "2015"},
        "price": {"N": "99.99"},
        "genre": {"S": "RPG"},
        "language": {"S": "polski"},
        "rating": {"N": "5"}
    }'

aws dynamodb get-item \
    --table-name MediaProducts-mateusz-skrobek \
    --key '{
        "product_id": {"S": "BOOK001"},
        "category": {"S": "książka"}
    }'


aws dynamodb scan \
    --table-name MediaProducts-mateusz-skrobek \
    --filter-expression "category = :cat" \
    --expression-attribute-values '{
        ":cat": {"S": "książka"}
    }'

aws dynamodb scan \
    --table-name MediaProducts-mateusz-skrobek \
    --filter-expression "rating = :r" \
    --expression-attribute-values '{
        ":r": {"N": "5"}
    }'


aws dynamodb scan \
    --table-name MediaProducts-mateusz-skrobek \
    --filter-expression "category = :cat" \
    --expression-attribute-values '{
        ":cat": {"S": "gra"}
    }'

aws dynamodb delete-item \
    --table-name MediaProducts-mateusz-skrobek \
    --key '{
        "product_id": {"S": "GAME001"},
        "category": {"S": "gra"}
    }'