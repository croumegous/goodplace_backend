-- upgrade --
ALTER TABLE "categories" ADD "icon" VARCHAR(50);
ALTER TABLE "categories" ADD "image" VARCHAR(500);
-- downgrade --
ALTER TABLE "categories" DROP COLUMN "icon";
ALTER TABLE "categories" DROP COLUMN "image";
