drop table if exists urls;
create table urls (
    short_url text primary key,
    long_url text not null
);
