-- Процедура добавления телефона
CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    SELECT id, p_phone, p_type FROM contacts WHERE name = p_name;
END;
$$ LANGUAGE plpgsql;

-- Поиск по всем полям (имя, почта, телефоны)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INTEGER, name VARCHAR, email VARCHAR, birthday DATE, phones TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, c.birthday, string_agg(p.phone, ', ')
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%' 
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id;
END;
$$ LANGUAGE plpgsql;
