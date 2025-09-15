-- Users
CREATE TABLE IF NOT EXISTS users (
  id           BIGSERIAL PRIMARY KEY,
  username     VARCHAR(50)  NOT NULL UNIQUE,
  password     TEXT         NOT NULL,
  fullname     VARCHAR(120) NOT NULL,
  email        VARCHAR(255) NOT NULL UNIQUE,
  cpf          VARCHAR(14)  NOT NULL UNIQUE,
  role         VARCHAR(20)  NOT NULL DEFAULT 'usuario',
  created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Movies
CREATE TABLE IF NOT EXISTS movies (
  id           BIGSERIAL PRIMARY KEY,
  title        VARCHAR(200) NOT NULL,
  duration     INTEGER      NOT NULL,
  genre        VARCHAR(80)  NOT NULL,
  description  TEXT,
  banner_url   TEXT,
  release_date DATE         NOT NULL,
  updated_at   TIMESTAMPTZ
);

-- Sessions
CREATE TABLE IF NOT EXISTS sessions (
  id          BIGSERIAL PRIMARY KEY,
  movie_id    BIGINT       NOT NULL REFERENCES movies(id) ON DELETE CASCADE,
  room        VARCHAR(20)  NOT NULL,
  start_time  TIMESTAMPTZ  NOT NULL,
  end_time    TIMESTAMPTZ  NOT NULL,
  updated_at  TIMESTAMPTZ
);
-- Índices úteis para consultas por horário/sala
CREATE INDEX IF NOT EXISTS idx_sessions_room ON sessions(room);
CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(start_time, end_time);

-- Seats
CREATE TABLE IF NOT EXISTS seats (
  id          BIGSERIAL PRIMARY KEY,
  session_id  BIGINT      NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  seat_number VARCHAR(10) NOT NULL,
  is_occupied BOOLEAN     NOT NULL DEFAULT FALSE,
  CONSTRAINT uq_seat_per_session UNIQUE(session_id, seat_number)
);

-- Tickets
CREATE TABLE IF NOT EXISTS tickets (
  id             BIGSERIAL PRIMARY KEY,
  user_id        BIGINT       NOT NULL REFERENCES users(id)    ON DELETE CASCADE,
  session_id     BIGINT       NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  seat_id        BIGINT       NOT NULL REFERENCES seats(id)    ON DELETE CASCADE,
  payment_status VARCHAR(20)  NOT NULL,
  payment_method VARCHAR(40),
  payment_id     VARCHAR(100),
  purchase_time  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_ticket_seat UNIQUE(seat_id)
);

-- Índices para listagens e joins
CREATE INDEX IF NOT EXISTS idx_tickets_user  ON tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_tickets_sess  ON tickets(session_id);
CREATE INDEX IF NOT EXISTS idx_seats_session ON seats(session_id);

-- Campos extras/ajustes (idempotentes)
ALTER TABLE movies   ADD COLUMN IF NOT EXISTS updated_at   TIMESTAMPTZ;
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS updated_at   TIMESTAMPTZ;
