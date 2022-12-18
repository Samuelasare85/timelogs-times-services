-- CreateTable
CREATE TABLE "Log" (
    "id" SERIAL NOT NULL,
    "time_in" TIMESTAMP(3),
    "time_out" TIMESTAMP(3),
    "user_id" INTEGER NOT NULL,

    CONSTRAINT "Log_pkey" PRIMARY KEY ("id")
);
