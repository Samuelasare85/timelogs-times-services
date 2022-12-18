/*
  Warnings:

  - Added the required column `indicator` to the `Log` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Log" ADD COLUMN     "absent" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "indicator" TEXT NOT NULL,
ALTER COLUMN "time_in" SET DEFAULT CURRENT_TIMESTAMP,
ALTER COLUMN "time_out" SET DEFAULT CURRENT_TIMESTAMP;
