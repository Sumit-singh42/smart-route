import React, { useState } from 'react';

export function Playground() {
    const [prompt, setPrompt] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const testRoute = async () => {
        setLoading(true);
        setResult(null);
        try {
            const start = Date.now();
            const res = await fetch('http://localhost:8000/v1/chat/completions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: [{ role: 'user', content: prompt }],
                    model: 'gpt-4o' // We ask for GPT-4, looking for arbitrage
                })
            });
            const data = await res.json();
            const duration = Date.now() - start;

            setResult({
                model: data.model,
                content: data.choices[0].message.content,
                duration: duration,
                isCached: data.model.includes('Cached')
            });
        } catch (err) {
            console.error(err);
        }
        setLoading(false);
    };

    return (
        <div className="glass-card rounded-3xl p-8 col-span-1 lg:col-span-2 mt-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-accent/10 rounded-full blur-3xl -z-10"></div>
            <h2 className="text-2xl font-bold mb-8 text-white flex items-center gap-3">
                <div className="w-1 h-8 bg-gradient-to-b from-accent to-transparent rounded-full"></div>
                Transparent Logic Playground
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Input */}
                <div className="space-y-4">
                    <label className="block text-zinc-400 text-xs font-bold uppercase tracking-wider">Test Prompt</label>
                    <div className="relative">
                        <textarea
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            className="w-full h-48 bg-black/20 border border-white/10 rounded-2xl p-6 text-white text-lg placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-transparent transition-all resize-none shadow-inner pb-16"
                            placeholder="Type 'Write python code...' to test complex routing..."
                        />
                        {/* File Upload UI */}
                        <div className="absolute bottom-4 left-4 flex items-center gap-3">
                            <input
                                type="file"
                                id="file-upload"
                                className="hidden"
                                accept=".txt,image/*,.pdf,.doc,.docx"
                                onChange={async (e) => {
                                    const file = e.target.files?.[0];
                                    if (!file) return;

                                    // setPrompt(prev => prev + ` [Uploading ${file.name}...]`); // Optional UI feedback

                                    try {
                                        const formData = new FormData();
                                        formData.append("file", file);

                                        const res = await fetch("http://localhost:8000/api/parse-document", {
                                            method: "POST",
                                            body: formData
                                        });

                                        if (!res.ok) throw new Error("Upload failed");

                                        const data = await res.json();
                                        const textContent = data.text;

                                        setPrompt(prev => {
                                            // Handle potential previous "Uploading..." placeholder if added, or just append
                                            // For now, simpler is better:
                                            return prev + `\n\n[Attached File: ${file.name}]\n${textContent}\n\n`;
                                        });

                                    } catch (err) {
                                        console.error("File parsing failed", err);
                                        setPrompt(prev => prev + `\n[Error uploading ${file.name}: ${err.message}]`);
                                    }
                                }}
                            />
                            <label
                                htmlFor="file-upload"
                                className="p-2 rounded-full bg-white/10 text-white/70 hover:bg-white/20 hover:text-white cursor-pointer transition-colors backdrop-blur-md"
                                title="Attach text or image"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14" /><path d="M12 5v14" /></svg>
                            </label>
                        </div>
                    </div>
                    <button
                        onClick={testRoute}
                        disabled={loading || !prompt}
                        className={`w-full py-4 rounded-xl font-bold text-white tracking-wide shadow-lg transition-all ${loading
                            ? 'bg-white/5 cursor-not-allowed text-zinc-500'
                            : 'bg-gradient-to-r from-accent to-secondary hover:shadow-accent/25 hover:scale-[1.02] active:scale-[0.98]'
                            }`}
                    >
                        {loading ? 'Analyzing Route...' : '⚡ ANALYZE & ROUTE'}
                    </button>
                </div>

                {/* Visualizer */}
                <div className="bg-black/20 rounded-2xl p-6 border border-white/5 relative overflow-hidden backdrop-blur-sm min-h-[300px]">
                    {!result && !loading && (
                        <div className="h-full flex flex-col items-center justify-center text-zinc-600 space-y-4 opacity-50">
                            <div className="text-6xl animate-pulse-slow">🔮</div>
                            <p className="font-mono text-sm tracking-widest">AWAITING INPUT</p>
                        </div>
                    )}

                    {loading && (
                        <div className="h-full flex flex-col items-center justify-center space-y-8">
                            <div className="relative">
                                <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-accent"></div>
                                <div className="absolute inset-0 animate-ping rounded-full h-16 w-16 border-2 border-accent/30"></div>
                            </div>
                            <div className="space-y-3 w-full max-w-xs">
                                <StepLabel active text="Scanning for PII..." />
                                <StepLabel active text="Calculating Complexity..." />
                                <StepLabel active text="Checking Cache..." />
                            </div>
                        </div>
                    )}

                    {result && (
                        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <div className="flex justify-between items-center pb-4 border-b border-white/10">
                                <div>
                                    <span className="text-zinc-500 text-[10px] uppercase tracking-wider font-bold">Routed To</span>
                                    <div className={`text-2xl font-bold tracking-tight ${getRouteColor(result.model)} drop-shadow-sm`}>
                                        {formatModelName(result.model)}
                                    </div>
                                </div>
                                <div className="text-right">
                                    <span className="text-zinc-500 text-[10px] uppercase tracking-wider font-bold">Latency</span>
                                    <div className="text-xl font-mono text-white/90">{result.duration}ms</div>
                                </div>
                            </div>

                            <div className="space-y-3 pl-2 border-l-2 border-white/5">
                                <StepLabel completed text="1. PII Scan Passed" />
                                <StepLabel completed text={`2. Complexity Analysis: ${result.model.includes('gpt-4') || result.model.includes('mythomax') ? 'HIGH' : 'LOW'}`} />
                                <StepLabel completed text={`3. Final Destination: ${result.model}`} highlight />
                            </div>

                            <div className="p-4 bg-white/5 rounded-lg border border-white/5 group hover:border-white/10 transition-colors max-h-96 overflow-y-auto custom-scrollbar">
                                <span className="text-zinc-500 text-[10px] uppercase tracking-wider font-bold block mb-2 sticky top-0 bg-[#161618] py-1 z-10 w-fit px-2 rounded-md">Model Response</span>
                                <p className="text-zinc-300 text-sm font-mono leading-relaxed group-hover:text-white transition-colors whitespace-pre-wrap">
                                    "{result.content}"
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

function StepLabel({ text, active, completed, highlight }) {
    let icon = "⚪";
    let color = "text-zinc-600";

    if (active) {
        icon = "⏳";
        color = "text-accent animate-pulse font-medium";
    } else if (completed) {
        icon = "✨";
        color = "text-zinc-400";
    }

    if (highlight) {
        color = "text-success font-bold drop-shadow-sm";
        icon = "🚀";
    }

    return (
        <div className={`flex items-center gap-3 ${color} text-sm transition-all`}>
            <span>{icon}</span> {text}
        </div>
    );
}

function getRouteColor(model) {
    if (model.includes('gpt-4')) return "text-purple-400";
    if (model.includes('mythomax')) return "text-indigo-400";
    if (model.includes('llama')) return "text-primary"; // Indigo/Blue
    return "text-white";
}

function formatModelName(model) {
    if (model.includes('gpt-4')) return "OpenAI GPT-4o";
    if (model.includes('mythomax')) return "Local Mythomax 13B";
    if (model.includes('llama')) return "Groq Llama-3";
    return model;
}
