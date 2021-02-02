-- upgrade --
ALTER TABLE "items" ADD "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "locations" ADD "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "users" ADD "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "items" ADD "text_search_vector" TSVECTOR;
CREATE INDEX IF NOT EXISTS idx_tsvector_items_tsv_gin
ON items
USING gin(text_search_vector);
DROP TRIGGER IF EXISTS tr_items_update_tsv ON items;
CREATE TRIGGER tr_items_update_tsv BEFORE INSERT OR UPDATE
ON items
FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger(text_search_vector, 'pg_catalog.english', title, description);
-- downgrade --
ALTER TABLE "items" DROP COLUMN "updated_at";
ALTER TABLE "locations" DROP COLUMN "updated_at";
ALTER TABLE "users" DROP COLUMN "updated_at";
ALTER TABLE "items" DROP COLUMN "text_search_vector";
DROP TRIGGER IF EXISTS tr_items_update_tsv ON items;
DROP INDEX IF EXISTS tsvector_items_description_title_gin;
