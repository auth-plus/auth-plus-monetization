-- migrate:up
INSERT INTO "event" ("type", "price")
VALUES ('EMAIL_AUTH_FACTOR_CREATED', 1.01);
INSERT INTO "event" ("type", "price")
VALUES ('PHONE_AUTH_FACTOR_CREATED', 1.02);
INSERT INTO "event" ("type", "price")
VALUES ('EMAIL_AUTH_FACTOR_SENT', 1.03);
INSERT INTO "event" ("type", "price")
VALUES ('PHONE_AUTH_FACTOR_SENT', 1.04);
INSERT INTO "event" ("type", "price")
VALUES ('USER_CREATED', 1.05);
INSERT INTO "event" ("type", "price")
VALUES ('ORGANIZATION_CREATED', 1.06);
-- migrate:down
DELETE FROM "event"
WHERE "type" = 'EMAIL_AUTH_FACTOR_CREATED';
DELETE FROM "event"
WHERE "type" = 'PHONE_AUTH_FACTOR_CREATED';
DELETE FROM "event"
WHERE "type" = 'EMAIL_AUTH_FACTOR_SENT';
DELETE FROM "event"
WHERE "type" = 'PHONE_AUTH_FACTOR_SENT';
DELETE FROM "event"
WHERE "type" = 'USER_CREATED';
DELETE FROM "event"
WHERE "type" = 'ORGANIZATION_CREATED';