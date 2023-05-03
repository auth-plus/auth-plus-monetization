-- migrate:up
INSERT INTO "event" ("type", "value")
VALUES ("2FA_EMAIL_CREATED", 1.01);
INSERT INTO "event" ("type", "value")
VALUES ("2FA_PHONE_CREATED", 1.02);
INSERT INTO "event" ("type", "value")
VALUES ("2FA_EMAIL_SENT", 1.03);
INSERT INTO "event" ("type", "value")
VALUES ("2FA_PHONE_SENT", 1.04);
INSERT INTO "event" ("type", "value")
VALUES ("USER_CREATED", 1.05);
INSERT INTO "event" ("type", "value")
VALUES ("ORGANIZATION_CREATED", 1.06);
-- migrate:down
DELETE FROM "event"
WHERE "type" = "2FA_EMAIL_CREATED";
DELETE FROM "event"
WHERE "type" = "2FA_PHONE_CREATED";
DELETE FROM "event"
WHERE "type" = "2FA_EMAIL_SENT";
DELETE FROM "event"
WHERE "type" = "2FA_PHONE_SENT";
DELETE FROM "event"
WHERE "type" = "USER_CREATED";
DELETE FROM "event"
WHERE "type" = "ORGANIZATION_CREATED";