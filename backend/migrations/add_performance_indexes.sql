-- Performance indexes for leads and interactions tables
-- Run this manually or via your migration tool

-- 1. HNSW index for vector similarity search (semantic search)
-- Dramatically speeds up cosine distance queries in search_leads
CREATE INDEX IF NOT EXISTS ix_leads_embedding_hnsw
    ON leads USING hnsw (embedding vector_cosine_ops);

-- 2. Composite index for Kanban column filtering + ordering
-- The kanban queries filter by status and sort by created_at desc
CREATE INDEX IF NOT EXISTS ix_leads_status_created_at
    ON leads (status, created_at DESC);

-- 3. Composite index for score-based filtering
-- list_leads filters by status and sorts by total_score
CREATE INDEX IF NOT EXISTS ix_leads_status_total_score
    ON leads (status, total_score DESC NULLS LAST);

-- 4. Composite index for discovery duplicate check
-- discover_leads checks duplicates by business_name + city
CREATE INDEX IF NOT EXISTS ix_leads_business_name_city
    ON leads (business_name, city);

-- 5. Composite index for interaction follow-up counts
-- Scheduled tasks count interactions by lead_id + type
CREATE INDEX IF NOT EXISTS ix_interactions_lead_type
    ON interactions (lead_id, interaction_type, created_at DESC);

-- 6. Partial indexes for email/phone/website presence checks
-- list_leads filters by has_email/has_phone/has_website
CREATE INDEX IF NOT EXISTS ix_leads_email_not_null
    ON leads (email) WHERE email IS NOT NULL AND email != '';
CREATE INDEX IF NOT EXISTS ix_leads_phone_not_null
    ON leads (phone) WHERE phone IS NOT NULL AND phone != '';
CREATE INDEX IF NOT EXISTS ix_leads_website_not_null
    ON leads (website) WHERE website IS NOT NULL AND website != '';
