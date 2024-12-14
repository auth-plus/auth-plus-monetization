-- migrate:up
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS "account" (
    "id" UUID NOT NULL DEFAULT Uuid_generate_v1(),
    "external_id" UUID NOT NULL,
    "type" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT Timezone('utc', Now()),
    "deleted_at" TIMESTAMP DEFAULT NULL,
    PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "subscription" (
    "id" UUID NOT NULL DEFAULT Uuid_generate_v1(),
    "account_id" UUID NOT NULL,
    "type" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT Timezone('utc', Now()),
    "deleted_at" TIMESTAMP DEFAULT NULL,
    PRIMARY KEY ("id"),
    CONSTRAINT fk_s_account_id FOREIGN KEY("account_id") REFERENCES "account"("id")
);
CREATE TYPE discount_type AS ENUM('PERCENTAGE', 'ABSOLUTE');
CREATE TABLE IF NOT EXISTS "discount" (
    "id" UUID NOT NULL DEFAULT Uuid_generate_v1(),
    "account_id" UUID NOT NULL,
    "reason" VARCHAR(255) NOT NULL,
    "amount" REAL NOT NULL,
    "type" discount_type NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT Timezone('utc', Now()),
    "deleted_at" TIMESTAMP DEFAULT NULL,
    PRIMARY KEY ("id"),
    CONSTRAINT fk_d_account_id FOREIGN KEY("account_id") REFERENCES "account"("id")
);
CREATE TABLE IF NOT EXISTS "ledger" (
    "id" UUID NOT NULL DEFAULT Uuid_generate_v1(),
    "account_id" UUID NOT NULL,
    "amount" REAL NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "price_id" UUID,
    "created_at" TIMESTAMP NOT NULL DEFAULT Timezone('utc', Now()),
    "deleted_at" TIMESTAMP DEFAULT NULL,
    PRIMARY KEY ("id"),
    CONSTRAINT fk_l_account_id FOREIGN KEY("account_id") REFERENCES "account"("id")
);
CREATE TABLE IF NOT EXISTS "price" (
    "id" UUID NOT NULL DEFAULT Uuid_generate_v1(),
    "event" TEXT NOT NULL,
    "value" NUMERIC(5, 2) NOT NULL,
    "created_at" TIMESTAMP DEFAULT Timezone('utc', Now()),
    "deleted_at" TIMESTAMP DEFAULT NULL,
    PRIMARY KEY ("id")
);
-- migrate:down
DROP TABLE "price";
DROP TABLE "ledger";
DROP TABLE "discount";
DROP TABLE "subscription";
DROP TABLE "account";