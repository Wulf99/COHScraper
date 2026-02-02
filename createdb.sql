CREATE DATABASE rwu_events;
USE rwu_events;

CREATE TABLE events (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,

  -- provenance
  source VARCHAR(100) NOT NULL,
  source_url TEXT,
  external_id VARCHAR(255) NOT NULL,

  -- core display
  title TEXT NOT NULL,
  description TEXT,
  link TEXT,

  -- time
  published_at DATETIME NULL,
  event_start DATETIME NULL,
  event_end DATETIME NULL,
  event_date_text VARCHAR(255),

  -- org / location
  location VARCHAR(255),
  organization VARCHAR(255),
  host VARCHAR(255),

  -- athletics-specific
  sport VARCHAR(50),
  opponent VARCHAR(255),
  is_conference BOOLEAN,
  status VARCHAR(50),

  -- metadata
  ingested_at DATETIME NOT NULL,

  -- constraints
  UNIQUE KEY uniq_source_external (source, external_id)
);
