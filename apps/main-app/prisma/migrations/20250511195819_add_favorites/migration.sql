-- CreateTable
CREATE TABLE "UserFavoriteHotels" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "userId" TEXT NOT NULL,
    "hotelId" UUID NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "UserFavoriteHotels_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "UserFavoriteHotels_userId_hotelId_key" ON "UserFavoriteHotels"("userId", "hotelId");

-- AddForeignKey
ALTER TABLE "UserFavoriteHotels" ADD CONSTRAINT "UserFavoriteHotels_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "UserFavoriteHotels" ADD CONSTRAINT "UserFavoriteHotels_hotelId_fkey" FOREIGN KEY ("hotelId") REFERENCES "hotels"("id") ON DELETE CASCADE ON UPDATE CASCADE;
