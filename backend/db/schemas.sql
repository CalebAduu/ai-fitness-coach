-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Profiles table
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    auth_user_id UUID,
    name VARCHAR(255) NOT NULL,
    sex VARCHAR(10) CHECK (sex IN ('male', 'female', 'other')),
    age INTEGER CHECK (age >= 13 AND age <= 120),
    height_cm INTEGER CHECK (height_cm >= 100 AND height_cm <= 250),
    weight_kg DECIMAL(5,2) CHECK (weight_kg >= 30 AND weight_kg <= 300),
    goals TEXT[],
    injuries TEXT[],
    equipment TEXT[],
    days_per_week INTEGER CHECK (days_per_week >= 1 AND days_per_week <= 7)
);

-- Plans table
CREATE TABLE IF NOT EXISTS plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    version INTEGER NOT NULL DEFAULT 1,
    kind VARCHAR(10) NOT NULL CHECK (kind IN ('workout', 'meal')),
    data JSONB NOT NULL,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, kind, version)
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    plan_version INTEGER NOT NULL,
    workout_day INTEGER NOT NULL,
    difficulty INTEGER NOT NULL CHECK (difficulty >= 1 AND difficulty <= 10),
    soreness INTEGER NOT NULL CHECK (soreness >= 0 AND soreness <= 10),
    pain BOOLEAN NOT NULL DEFAULT false,
    enjoyment INTEGER NOT NULL CHECK (enjoyment >= 1 AND enjoyment <= 5),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_profiles_auth_user_id ON profiles(auth_user_id);
CREATE INDEX IF NOT EXISTS idx_plans_user_id ON plans(user_id);
CREATE INDEX IF NOT EXISTS idx_plans_user_kind_active ON plans(user_id, kind, active);
CREATE INDEX IF NOT EXISTS idx_plans_version_desc ON plans(user_id, version DESC);
CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_feedback_plan_version ON feedback(user_id, plan_version);

-- Row Level Security (RLS) policies
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth_user_id = auth.uid());

CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth_user_id = auth.uid());

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth_user_id = auth.uid());

-- Plans policies
CREATE POLICY "Users can view own plans" ON plans
    FOR SELECT USING (user_id IN (
        SELECT id FROM profiles WHERE auth_user_id = auth.uid()
    ));

CREATE POLICY "Users can insert own plans" ON plans
    FOR INSERT WITH CHECK (user_id IN (
        SELECT id FROM profiles WHERE auth_user_id = auth.uid()
    ));

CREATE POLICY "Users can update own plans" ON plans
    FOR UPDATE USING (user_id IN (
        SELECT id FROM profiles WHERE auth_user_id = auth.uid()
    ));

CREATE POLICY "Users can delete own plans" ON plans
    FOR DELETE USING (user_id IN (
        SELECT id FROM profiles WHERE auth_user_id = auth.uid()
    ));

-- Feedback policies
CREATE POLICY "Users can view own feedback" ON feedback
    FOR SELECT USING (user_id IN (
        SELECT id FROM profiles WHERE auth_user_id = auth.uid()
    ));

CREATE POLICY "Users can insert own feedback" ON feedback
    FOR INSERT WITH CHECK (user_id IN (
        SELECT id FROM profiles WHERE auth_user_id = auth.uid()
    ));

CREATE POLICY "Users can update own feedback" ON feedback
    FOR UPDATE USING (user_id IN (
        SELECT id FROM profiles WHERE auth_user_id = auth.uid()
    ));

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
