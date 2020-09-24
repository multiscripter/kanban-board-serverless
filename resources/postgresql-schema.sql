CREATE TABLE tasks (
    id smallserial NOT NULL PRIMARY KEY,
    title character varying(64) NOT NULL,
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    status smallint NOT NULL,
    payment real NOT NULL,
    CONSTRAINT tasks_payment_check CHECK (payment > -1),
    CONSTRAINT tasks_status_check CHECK (status > -1 AND status < 3)
);