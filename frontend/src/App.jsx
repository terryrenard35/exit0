import React, { useState, useEffect } from 'react';
import { db } from './firebase'; 
import { collection, getDocs, addDoc } from 'firebase/firestore'; 
import Auth from './components/Auth';
import { useAuth } from './hooks/useAuth';
import { 
  Server, Shield, Box, Cloud, Terminal, 
  Database, Cpu, Search, Copy, Check, Plus, Trash2, Image as ImageIcon
} from 'lucide-react';

function App() {
  const { user } = useAuth();
  const [tech, setTech] = useState('');
  const [problem, setProblem] = useState('');
  const [foundSolution, setFoundSolution] = useState(null);
  const [loadingSearch, setLoadingSearch] = useState(false);
  const [supportedApps, setSupportedApps] = useState([]);
  const [copiedId, setCopiedId] = useState(null);

  // États pour le formulaire de contribution multi-blocs
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newApp, setNewApp] = useState('');
  const [procedureBlocks, setProcedureBlocks] = useState([{ type: 'text', content: '' }]);

  const getIcon = (name) => {
    const n = name.toLowerCase();
    if (n.includes('directory') || n.includes('active')) return <Shield size={20} />;
    if (n.includes('docker') || n.includes('kube')) return <Box size={20} />;
    if (n.includes('aws') || n.includes('cloud') || n.includes('azure')) return <Cloud size={20} />;
    if (n.includes('linux') || n.includes('ubuntu')) return <Terminal size={20} />;
    if (n.includes('db') || n.includes('sql') || n.includes('mongo')) return <Database size={20} />;
    if (n.includes('server') || n.includes('apache') || n.includes('nginx')) return <Server size={20} />;
    return <Cpu size={20} />;
  };

  useEffect(() => {
    const fetchApps = async () => {
      try {
        const querySnapshot = await getDocs(collection(db, "applications"));
        const names = querySnapshot.docs.map(doc => doc.id); 
        setSupportedApps([...new Set(names)].sort());
      } catch (err) { console.error(err); }
    };
    fetchApps();
  }, [foundSolution, isModalOpen]);

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    setLoadingSearch(true);
    setFoundSolution(null);
    try {
      const querySnapshot = await getDocs(collection(db, "applications"));
      const allApps = querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      const sTech = tech.toLowerCase().trim();
      const sProb = problem.toLowerCase().trim();
      let match = null;

      for (const app of allApps) {
        if (app.id.toLowerCase().includes(sTech)) {
          if (app.solutions) {
            const solMatch = app.solutions.find(s => {
              const content = s.blocks ? s.blocks.map(b => b.content).join(' ').toLowerCase() : "";
              return content.includes(sProb);
            });
            if (solMatch) {
              match = { appName: app.id, author: solMatch.author, blocks: solMatch.blocks };
              break;
            }
          }
        }
      }
      setFoundSolution(match);
    } catch (err) { console.error(err); }
    setLoadingSearch(false);
  };

  // Gestion des blocs de contribution
  const addBlock = (type) => setProcedureBlocks([...procedureBlocks, { type, content: '' }]);
  const removeBlock = (index) => setProcedureBlocks(procedureBlocks.filter((_, i) => i !== index));
  const updateBlock = (index, value) => {
    const newBlocks = [...procedureBlocks];
    newBlocks[index].content = value;
    setProcedureBlocks(newBlocks);
  };

  const handleContribute = async (e) => {
    e.preventDefault();
    try {
      await addDoc(collection(db, "applications"), {
        application: newApp.toLowerCase(),
        solutions: [{
          author: user.displayName,
          blocks: procedureBlocks
        }]
      });
      setIsModalOpen(false);
      setNewApp('');
      setProcedureBlocks([{ type: 'text', content: '' }]);
      alert("SYSTÈME_MIS_À_JOUR");
    } catch (err) { alert(err.message); }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredApps = supportedApps.filter(app => 
    app.toLowerCase().includes(tech.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-[#e0e0e0] font-mono p-4 md:p-10">
      <header className="max-w-5xl mx-auto flex justify-between items-center mb-10 border-b border-[#2ecc71]/10 pb-6">
        <div className="flex items-center gap-4">
          <div className="bg-[#2ecc71] text-[#0a0a0a] p-2 rounded-lg font-bold text-2xl shadow-[0_0_15px_rgba(46,204,113,0.3)]">{'>_'}</div>
          <h1 className="text-3xl font-black uppercase italic tracking-tighter">EXIT<span className="text-[#2ecc71]">0</span></h1>
        </div>
        <Auth />
      </header>

      <main className="max-w-5xl mx-auto">
        <div className="mb-10">
          <div className="flex justify-between items-end mb-4">
            <h2 className="text-[10px] text-[#444] uppercase font-bold tracking-[0.3em]">Systèmes_Indexés</h2>
            {user && (
              <button onClick={() => setIsModalOpen(true)} className="flex items-center gap-2 text-[10px] font-bold text-[#2ecc71] border border-[#2ecc71]/30 px-3 py-1 rounded hover:bg-[#2ecc71] hover:text-black transition-all">
                <Plus size={12} /> NOUVELLE_PROCÉDURE
              </button>
            )}
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-6 gap-3">
            {filteredApps.map(appName => (
              <button key={appName} onClick={() => setTech(appName)} className={`flex flex-col items-center justify-center p-4 rounded-xl border transition-all duration-200 ${tech.toLowerCase() === appName.toLowerCase() ? "bg-[#2ecc71]/10 border-[#2ecc71] text-[#2ecc71]" : "bg-[#111] border-[#222] text-[#555] hover:border-[#333]"}`}>
                <div className="mb-2">{getIcon(appName)}</div>
                <span className="text-[10px] font-bold uppercase truncate w-full text-center">{appName}</span>
              </button>
            ))}
          </div>
        </div>

        {/* MODALE DE CONTRIBUTION MULTI-BLOCS */}
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-md p-4 overflow-y-auto">
            <div className="bg-[#111] border border-[#2ecc71] p-8 rounded-2xl max-w-2xl w-full my-auto shadow-2xl">
              <h2 className="text-[#2ecc71] font-bold mb-6 uppercase italic tracking-tighter underline">Éditeur de Procédure Ops</h2>
              <form onSubmit={handleContribute} className="space-y-6">
                <input required placeholder="Nom App (ex: kubernetes)" value={newApp} onChange={e=>setNewApp(e.target.value)} className="w-full bg-black border border-[#222] p-4 rounded-xl text-[#2ecc71] outline-none focus:border-[#2ecc71]" />
                <div className="space-y-4 max-h-[40vh] overflow-y-auto pr-2 custom-scrollbar">
                  {procedureBlocks.map((block, idx) => (
                    <div key={idx} className="relative group flex items-start gap-2">
                      <div className="flex-1">
                        {block.type === 'text' ? (
                          <textarea required placeholder="Description ou étape..." value={block.content} onChange={e=>updateBlock(idx, e.target.value)} className="w-full bg-black border border-[#222] p-3 rounded-lg text-[#aaa] min-h-[80px] outline-none focus:border-[#2ecc71]/50" />
                        ) : (
                          <input required placeholder="Commande shell..." value={block.content} onChange={e=>updateBlock(idx, e.target.value)} className="w-full bg-black border border-[#2ecc71]/20 p-3 rounded-lg text-[#2ecc71] font-mono outline-none focus:border-[#2ecc71]" />
                        )}
                      </div>
                      <button type="button" onClick={() => removeBlock(idx)} className="p-2 text-[#333] hover:text-red-500 transition-colors"><Trash2 size={16} /></button>
                    </div>
                  ))}
                </div>
                <div className="flex gap-2 border-t border-[#222] pt-4">
                  <button type="button" onClick={() => addBlock('text')} className="text-[9px] border border-[#333] px-3 py-2 rounded text-[#888] hover:text-[#2ecc71] tracking-widest">+ TEXTE</button>
                  <button type="button" onClick={() => addBlock('code')} className="text-[9px] border border-[#333] px-3 py-2 rounded text-[#888] hover:text-[#2ecc71] tracking-widest">+ CODE</button>
                </div>
                <div className="flex gap-4 pt-4 border-t border-[#222]">
                  <button type="submit" className="flex-1 bg-[#2ecc71] text-black font-black p-4 rounded-xl uppercase text-xs">Déployer la Procédure</button>
                  <button type="button" onClick={()=>setIsModalOpen(false)} className="flex-1 border border-red-900/30 text-red-500 font-bold p-4 rounded-xl uppercase text-xs">Annuler</button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="bg-[#111] border border-[#222] rounded-2xl p-6 mb-10 relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 left-0 w-1 h-full bg-[#2ecc71]"></div>
          <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4 items-end">
            <div className="flex-1 w-full"><label className="text-[10px] text-[#444] uppercase mb-2 block font-bold">Target_Tech</label><input type="text" value={tech} onChange={e=>setTech(e.target.value)} placeholder="Technologie..." className="w-full bg-[#0a0a0a] border border-[#222] p-4 rounded-xl text-[#2ecc71] outline-none" /></div>
            <div className="flex-[1.5] w-full"><label className="text-[10px] text-[#444] uppercase mb-2 block font-bold">Search_Query</label><input type="text" value={problem} onChange={e=>setProblem(e.target.value)} placeholder="Problème..." className="w-full bg-[#0a0a0a] border border-[#222] p-4 rounded-xl text-white outline-none" /></div>
            <button type="submit" className="w-full md:w-auto bg-[#2ecc71] text-[#0a0a0a] font-black px-8 py-4 rounded-xl uppercase text-sm flex items-center justify-center gap-2">{loadingSearch ? <span className="animate-pulse">RUNNING...</span> : <><Search size={18} /> Rechercher</>}</button>
          </form>
        </div>

        {foundSolution ? (
          <div className="bg-[#111] border border-[#222] p-8 rounded-2xl shadow-2xl animate-in zoom-in-95">
            <div className="flex justify-between items-start mb-8">
              <span className="text-[10px] bg-[#2ecc71]/10 text-[#2ecc71] px-2 py-1 rounded border border-[#2ecc71]/20 font-bold uppercase tracking-widest">Verified_Solution</span>
              <p className="text-[#2ecc71] text-xs font-bold uppercase tracking-widest">{foundSolution.appName}</p>
            </div>
            <div className="space-y-4">
              {foundSolution.blocks.map((block, idx) => (
                <div key={idx} className={block.type === 'text' ? "text-[#aaa] italic leading-relaxed" : "bg-[#050505] p-6 rounded-xl border border-[#222] relative group"}>
                  {block.type === 'text' ? (
                    <p>{block.content}</p>
                  ) : (
                    <>
                      <button type="button" onClick={() => copyToClipboard(block.content, idx)} className="absolute top-3 right-4 p-2 rounded-md hover:bg-[#2ecc71]/10 text-[#333] hover:text-[#2ecc71] transition-all">{copiedId === idx ? <Check size={14} /> : <Copy size={14} />}</button>
                      <code className="text-[#2ecc71] text-sm md:text-base block pr-10">$ {block.content}</code>
                    </>
                  )}
                </div>
              ))}
            </div>
          </div>
        ) : (
          (tech || problem) && !loadingSearch && (
            <div className="text-center py-20 border-2 border-dashed border-[#111] rounded-3xl text-[#333] uppercase font-bold tracking-widest">No_Data_Found</div>
          )
        )}
      </main>
    </div>
  );
}

export default App;
