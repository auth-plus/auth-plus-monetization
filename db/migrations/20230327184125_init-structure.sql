-- migrate:up
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "client" (
    "id" UUID not null default uuid_generate_v1(),
    "external_id" UUID not null,
    "plan_type" varchar(64) not null,
    "is_enable" boolean not null default TRUE,
    "created_at" timestamp not null default timezone('utc', now()),
    PRIMARY KEY ("id")
)

-- migrate:down

DROP TABLE "client";