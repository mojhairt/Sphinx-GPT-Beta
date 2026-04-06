import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

// Handle environment variables safely across different serve methods
let supabaseUrl = '';
let supabaseAnonKey = '';

if (typeof import.meta !== 'undefined' && import.meta.env) {
    // Vite environment
    supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
    supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;
}

if (!supabaseUrl || !supabaseAnonKey) {
    console.warn('Supabase configuration missing! Waiting for proper environment variables...');
    // Provide safe defaults to prevent crashing, but DO NOT use production secrets here!
    supabaseUrl = supabaseUrl || 'https://example-placeholder.supabase.co';
    supabaseAnonKey = supabaseAnonKey || 'placeholder-key';
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)