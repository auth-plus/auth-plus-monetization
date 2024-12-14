-- migrate:up
INSERT INTO "price" ("event", "value")
VALUES ('EMAIL_AUTH_FACTOR_CREATED', 1.01);
INSERT INTO "price" ("event", "value")
VALUES ('PHONE_AUTH_FACTOR_CREATED', 1.02);
INSERT INTO "price" ("event", "value")
VALUES ('EMAIL_AUTH_FACTOR_SENT', 1.03);
INSERT INTO "price" ("event", "value")
VALUES ('PHONE_AUTH_FACTOR_SENT', 1.04);
INSERT INTO "price" ("event", "value")
VALUES ('USER_CREATED', 1.05);
INSERT INTO "price" ("event", "value")
VALUES ('ORGANIZATION_CREATED', 1.06);
-- migrate:down
DELETE FROM "price"
WHERE "event" = 'EMAIL_AUTH_FACTOR_CREATED';
DELETE FROM "price"
WHERE "event" = 'PHONE_AUTH_FACTOR_CREATED';
DELETE FROM "price"
WHERE "event" = 'EMAIL_AUTH_FACTOR_SENT';
DELETE FROM "price"
WHERE "event" = 'PHONE_AUTH_FACTOR_SENT';
DELETE FROM "price"
WHERE "event" = 'USER_CREATED';
DELETE FROM "price"
WHERE "event" = 'ORGANIZATION_CREATED';