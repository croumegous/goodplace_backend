-- upgrade --
CREATE TABLE IF NOT EXISTS "categories" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "label" VARCHAR(50) NOT NULL UNIQUE
);
COMMENT ON TABLE "categories" IS 'Represent the category of the ad, for example \"car\", \"toys\", \"gardening\" ...';
CREATE TABLE IF NOT EXISTS "conditions" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "label" VARCHAR(50) NOT NULL UNIQUE
);
COMMENT ON TABLE "conditions" IS 'Represent the condition of the object/content of the ad, this field is not mandatory';
CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "phone_number" VARCHAR(20)  UNIQUE,
    "nickname" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(60) NOT NULL,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "avatar_url" VARCHAR(500),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "users" IS 'User represent a user account, it is necessary to create items';
CREATE TABLE IF NOT EXISTS "items" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "title" VARCHAR(50) NOT NULL,
    "description" VARCHAR(5000) NOT NULL,
    "price" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "category_id" UUID NOT NULL REFERENCES "categories" ("id") ON DELETE CASCADE,
    "condition_id" UUID REFERENCES "conditions" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "items" IS 'Represent an ad, someting to be sold by the user who create this ad';
CREATE TABLE IF NOT EXISTS "images" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "image_url" VARCHAR(500) NOT NULL,
    "item_id" UUID NOT NULL REFERENCES "items" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "images" IS 'Image represent the url image used to highlight an item';
CREATE TABLE IF NOT EXISTS "locations" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "country" VARCHAR(50) NOT NULL,
    "state" VARCHAR(50),
    "city" VARCHAR(50) NOT NULL,
    "street" VARCHAR(100) NOT NULL,
    "street_number" VARCHAR(20),
    "address_complement" VARCHAR(100),
    "postal_code" VARCHAR(20) NOT NULL
);
ALTER TABLE "locations" ADD "user_id" UUID NOT NULL UNIQUE;
ALTER TABLE "locations" ADD CONSTRAINT "fk_location_users" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
COMMENT ON TABLE "locations" IS 'Location represent a the location of an user useful to find near items';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
