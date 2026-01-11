import React, { useEffect, useState } from 'react';
import { Playground } from './components/Playground';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Routes, Route, Navigate } from 'react-router-dom';
import { SignedIn, SignedOut, SignIn, SignUp, RedirectToSignIn } from '@clerk/clerk-react';

function Dashboard() {
    const [stats, setStats] = useState({
        requests: 0,
        savings: 0,
        hit_rate: 0,
        provider_groq: 0,
        provider_local: 0
    });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await fetch('http://localhost:8000/api/stats');
                const data = await res.json();
                console.log("Stats Poll:", data);
                if (data) {
                    setStats(prev => ({
                        ...prev,
                        ...data,
                        // Ensure nested object is merged correctly if needed, though API returns full latest_request
                        latest_request: data.latest_request || prev.latest_request
                    }));
                }
            } catch (err) {
                console.error("Failed to fetch stats", err);
            }
        };

        const interval = setInterval(fetchStats, 1000); // Increased polling freq to 1s for "real-time" feel
        fetchStats(); // Initial fetch
        return () => clearInterval(interval);
    }, []);

    const purgeCache = async () => {
        if (!confirm("Are you sure you want to purge the cache? This will reset all stats.")) return;
        try {
            await fetch('http://localhost:8000/api/cache/clear', { method: 'POST' });
            setStats({
                requests: 0,
                savings: 0,
                hit_rate: 0,
                provider_groq: 0,
                provider_local: 0
            });
        } catch (err) {
            console.error("Failed to purge cache", err);
        }
    };

    return (
        <div className="min-h-screen p-8 font-sans selection:bg-primary/30">
            {/* Background Animations */}
            <div className="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-primary/20 rounded-full blur-[100px] animate-blob"></div>
                <div className="absolute top-[20%] right-[-10%] w-96 h-96 bg-secondary/20 rounded-full blur-[100px] animate-blob animation-delay-2000"></div>
                <div className="absolute bottom-[-10%] left-[20%] w-96 h-96 bg-accent/20 rounded-full blur-[100px] animate-blob animation-delay-4000"></div>
            </div>

            <header className="mb-12 border-b border-white/5 pb-8 relative flex flex-col md:flex-row justify-between items-center gap-6">
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent h-[1px] bottom-0"></div>

                {/* Logo Section */}
                <div className="flex items-center gap-6">
                    <img
                        src="/logo.png?v=6"
                        alt="SmartRoute AI Logo"
                        className="h-20 w-auto object-contain drop-shadow-2xl hover:scale-105 transition-transform duration-300"
                    />
                    <div className="h-12 w-[1px] bg-white/10 hidden md:block"></div>
                    <div className="hidden md:block">
                        <h1 className="text-4xl font-display font-extrabold text-white tracking-tight">
                            SmartRoute AI
                        </h1>
                        <p className="text-zinc-400 text-sm font-light tracking-wide mt-1">
                            Intelligent LLM Arbitrage Engine
                        </p>
                    </div>
                </div>

                <div className="flex gap-3">
                    <StatusBadge label="SYSTEM ONLINE" color="emerald" pulse />
                    <StatusBadge label="LOCAL MODE" color="indigo" />
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                {/* Metric Cards */}
                <MetricCard title="Total Requests" value={stats.requests} icon="📊" />
                <MetricCard
                    title="Est. Savings"
                    value={`$${(stats.savings || 0).toFixed(4)}`}
                    subValue="vs Pure GPT-4o"
                    success
                    icon="💰"
                />
                <MetricCard
                    title="Cache Hit Rate"
                    value={`${stats.hit_rate}%`}
                    icon="⚡"
                    action={
                        <button
                            onClick={purgeCache}
                            className="absolute bottom-4 right-4 p-2 rounded-full bg-red-500/10 text-red-500 hover:bg-red-500/20 transition-colors"
                            title="Purge Cache"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18" /><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" /><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" /></svg>
                        </button>
                    }
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
                <div className="glass-card glass-card-hover rounded-3xl p-8 relative overflow-hidden group">
                    <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <h2 className="text-2xl font-bold mb-6 text-white flex items-center gap-3">
                        <div className="w-1 h-8 bg-gradient-to-b from-cyan-400 to-transparent rounded-full"></div>
                        Model Distribution
                    </h2>
                    <div className="h-64 flex items-center justify-center text-zinc-500 bg-black/20 rounded-2xl border border-white/5 backdrop-blur-sm overflow-hidden p-2">
                        {stats.requests > 0 ? (
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={[
                                            { name: 'Groq (Fast)', value: stats.provider_groq || 0 },
                                            { name: 'Local (Free)', value: stats.provider_local || 0 },
                                            { name: 'Cached', value: stats.cache_hits || 0 },
                                        ]}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={60}
                                        outerRadius={80}
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        <Cell fill="#06b6d4" stroke="none" /> {/* Cyan - Groq */}
                                        <Cell fill="#ec4899" stroke="none" /> {/* Pink - Local */}
                                        <Cell fill="#10b981" stroke="none" /> {/* Green - Cache */}
                                    </Pie>
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#0f0c29', borderColor: '#ffffff20', borderRadius: '12px' }}
                                        itemStyle={{ color: '#e0e7ff' }}
                                    />
                                    <Legend verticalAlign="bottom" height={36} iconType="circle" />
                                </PieChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="flex flex-col items-center gap-2 opacity-50">
                                <span className="text-4xl">🍩</span>
                                <p className="font-mono text-sm">Waiting for data...</p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="glass-card glass-card-hover rounded-3xl p-8 relative overflow-hidden group">
                    <div className="absolute inset-0 bg-gradient-to-b from-secondary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <h2 className="text-2xl font-bold mb-6 text-white flex items-center gap-3">
                        <div className="w-1 h-8 bg-gradient-to-b from-secondary to-transparent rounded-full"></div>
                        Live Dispatcher
                    </h2>
                    <div className="space-y-3 font-mono text-sm max-h-64 overflow-y-auto pr-2 custom-scrollbar">
                        {!stats.latest_request || stats.latest_request.provider === "Waiting..." ? (
                            <div className="text-zinc-600 italic text-center py-10">Waiting for incoming traffic...</div>
                        ) : (
                            <div className="p-4 bg-white/5 border border-white/10 rounded-xl flex justify-between items-center text-zinc-300 animate-in fade-in slide-in-from-right duration-300 hover:bg-white/10 transition-colors">
                                <div className="flex flex-col gap-1">
                                    <span className="text-[10px] text-zinc-500 uppercase tracking-wider">Latest Request</span>
                                    <span className="flex items-center gap-2">
                                        <span className={`w-2 h-2 rounded-full ${stats.latest_request.provider.includes("LOCAL") ? "bg-pink-500" : "bg-cyan-500"}`}></span>
                                        {stats.latest_request.type}
                                    </span>
                                </div>
                                <span className={`px-3 py-1 rounded-full text-xs font-bold ${stats.latest_request.provider.includes("LOCAL")
                                    ? "bg-pink-500/20 text-pink-400 border border-pink-500/20"
                                    : "bg-cyan-500/20 text-cyan-400 border border-cyan-500/20"
                                    }`}>
                                    → {stats.latest_request.provider}
                                </span>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <Playground />
        </div>
    );
}

function MetricCard({ title, value, subValue, success, icon, action }) {
    return (
        <div className="glass-card glass-card-hover p-8 rounded-3xl relative overflow-hidden group">
            <div className="absolute -right-6 -top-6 w-24 h-24 bg-gradient-to-br from-white/10 to-transparent rounded-full blur-xl group-hover:scale-150 transition-transform duration-700"></div>
            <div className="relative z-10">
                <div className="flex justify-between items-start mb-4">
                    <h3 className="text-zinc-400 text-xs font-bold uppercase tracking-widest">{title}</h3>
                    <span className="text-2xl opacity-50 grayscale group-hover:grayscale-0 transition-all">{icon}</span>
                </div>
                <div className="text-5xl font-display font-bold text-white tracking-tight drop-shadow-sm group-hover:text-glow transition-all">{value}</div>
                {subValue && (
                    <div className={`text-sm mt-3 font-medium flex items-center gap-1 ${success ? 'text-success' : 'text-zinc-500'}`}>
                        {success && <span className="text-success">▲</span>}
                        {subValue}
                    </div>
                )}
                {action}
            </div>
        </div>
    );
}

function StatusBadge({ label, color, pulse }) {
    const colors = {
        emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
        indigo: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
    };

    return (
        <span className={`px-3 py-1.5 rounded-full text-[10px] font-bold tracking-wider border flex items-center gap-2 ${colors[color] || colors.emerald}`}>
            {pulse && <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse"></span>}
            {label}
        </span>
    )
}

function App() {
    return (
        <Routes>
            <Route
                path="/sign-in/*"
                element={
                    <div className="min-h-screen flex items-center justify-center bg-[#0f0c29]">
                        <SignIn routing="path" path="/sign-in" />
                    </div>
                }
            />
            <Route
                path="/sign-up/*"
                element={
                    <div className="min-h-screen flex items-center justify-center bg-[#0f0c29]">
                        <SignUp routing="path" path="/sign-up" />
                    </div>
                }
            />
            <Route
                path="/"
                element={
                    <>
                        <SignedIn>
                            <Dashboard />
                        </SignedIn>
                        <SignedOut>
                            <RedirectToSignIn />
                        </SignedOut>
                    </>
                }
            />
        </Routes>
    );
}

export default App;
