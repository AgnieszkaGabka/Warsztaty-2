CREATE TABLE public.Users
(
    id integer not null primary key,
    username varchar(255),
    hashed_password varchar(80)
);