CREATE EXTENSION IF NOT EXISTS vector;


-- CreateTable
CREATE TABLE "document_embeddings" (
    "id" INTEGER NOT NULL,
    "embedding" vector NOT NULL,

    CONSTRAINT "document_embeddings_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "documents" (
    "id" INTEGER NOT NULL,
    "title" TEXT NOT NULL,
    "content" TEXT NOT NULL,

    CONSTRAINT "documents_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "hotels" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "country_code" VARCHAR(10) NOT NULL,
    "country_name" VARCHAR(100) NOT NULL,
    "city_code" VARCHAR(10) NOT NULL,
    "city_name" VARCHAR(100) NOT NULL,
    "hotel_code" VARCHAR(100),
    "hotel_name" VARCHAR(200) NOT NULL,
    "hotel_rating" VARCHAR(50),
    "address" TEXT,
    "attractions" TEXT,
    "description" TEXT,
    "fax_number" VARCHAR(200),
    "hotel_facilities" TEXT,
    "map_position" VARCHAR(100),
    "phone_number" VARCHAR(100),
    "pin_code" VARCHAR(30),
    "hotel_website_url" VARCHAR(255),
    "embedding" vector,
    "metadata" JSONB,

    CONSTRAINT "hotels_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "document_embeddings_embedding_idx" ON "document_embeddings"("embedding");

-- CreateIndex
CREATE INDEX "hotels_embeddings_idx" ON "hotels"("embedding");

