DO $$
DECLARE
    max_id INT;
BEGIN
    -- Find the maximum id in the General_States table
    SELECT COALESCE(MAX(id), 0) INTO max_id FROM "General_States";

    -- Update the sequence value to max_id + 1
    PERFORM setval('"General_States_id_seq"', max_id + 1);

    -- Optionally, you can print out the new sequence value to verify
    RAISE NOTICE 'Sequence set to %', max_id + 1;
END $$;
DO $$
DECLARE
    max_id INT;
BEGIN
    -- Find the maximum id in the General_States table
    SELECT COALESCE(MAX(id), 0) INTO max_id FROM "General_States";

    -- Print the maximum id value
    RAISE NOTICE 'The maximum id in the General_States table is %', max_id;
END $$;
DO $$
DECLARE
    seq_value INT;
BEGIN
    -- Get the current value of the sequence
    SELECT last_value INTO seq_value FROM "General_States_id_seq";

    -- Print the current value of the sequence
    RAISE NOTICE 'The current value of General_States_id_seq is %', seq_value;
EXCEPTION
    WHEN undefined_table THEN
        RAISE NOTICE 'Sequence not yet used in this session.';
END $$;
