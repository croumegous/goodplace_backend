-- upgrade --
CREATE OR REPLACE FUNCTION func_delete_items_on_delete_location()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS 
  'BEGIN
	DELETE FROM items 
	WHERE items.user_id = OLD.user_id; 
	RETURN OLD; 
    END;';
CREATE TRIGGER delete_items_on_delete_location
  AFTER DELETE
  ON locations
  FOR EACH ROW
  EXECUTE PROCEDURE func_delete_items_on_delete_location();
-- downgrade --
DROP TRIGGER delete_items_on_delete_location ON locations;
DROP FUNCTION func_delete_items_on_delete_location;