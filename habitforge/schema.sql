-- Run this once in Supabase: SQL Editor -> New query -> paste -> Run

create table if not exists public.user_state (
  user_id uuid primary key references auth.users(id) on delete cascade,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.user_state enable row level security;

-- Each user can only see and change their own row.
create policy "read own state" on public.user_state
  for select using (auth.uid() = user_id);

create policy "insert own state" on public.user_state
  for insert with check (auth.uid() = user_id);

create policy "update own state" on public.user_state
  for update using (auth.uid() = user_id);
