-- migrate:up
ALTER TABLE "account" DROP COLUMN "type";

-- migrate:down

ALTER TABLE "account" ADD "type" VARCHAR(20) NOT NULL