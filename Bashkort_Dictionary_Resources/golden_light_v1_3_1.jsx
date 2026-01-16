import React, { useState } from 'react';
import { Sun, Home, Scroll, Compass, Map, Languages, Lightbulb, Quote, History, BookOpen, FileText, ChevronDown, ChevronLeft, ChevronRight, Mountain, Bird, Sword, Flame, TreePine, Waves, Droplets, Shield, Crown, Star, Heart, Filter, Award, Scale, Flag, Users, Zap } from 'lucide-react';

// ═══════════════════════════════════════════════════════════════════════════════
// АЛТЫН ЯҠТЫ — GOLDEN LIGHT v1.3.1
// The Legacy Edition with v1.1 Visual Style
// "Кешеләр тәндәре менән түгел, ә изге эштәре менән мәңге йәшәйҙәр"
// ═══════════════════════════════════════════════════════════════════════════════

const LEGACY_PROVERB = {
  bashkir: "Кешеләр тәндәре менән түгел, ә изге эштәре менән мәңге йәшәйҙәр",
  english: "People live forever not through their bodies, but through their good deeds",
  russian: "Люди живут вечно не телом, а добрыми делами",
  phonetic: "ke-she-LAR tan-da-RE me-NAN tu-GEL, a iz-GE esh-ta-RE me-NAN man-GE ya-sha-Y-zar"
};

// ═══════════════════════════════════════════════════════════════════════════════
// EPIC DATA - 10 Chapters
// ═══════════════════════════════════════════════════════════════════════════════
const epicChapters = [
  { id: 1, title: "The Birth of Heroes", bashkir: "Батырҙарҙың тыуыуы", icon: Home, color: "from-emerald-800 to-emerald-600",
    summary: "Yanbirde and Yanbike raise two sons: Shulgen and Ural",
    text: `Long ago, when the world was young and the mountains had not yet risen to touch the sky, there lived an old man named Yanbirde and his wife Yanbike. They dwelt alone in a vast wilderness, knowing nothing of other humans.\n\nThe couple was blessed with two sons. The elder they named Shulgen, and the younger they called Ural. From their earliest days, the brothers showed different natures—Shulgen was bold and impetuous, while Ural was thoughtful and kind.\n\nYanbirde taught his sons the ways of survival and shared with them the great mystery—the existence of Death, the great destroyer who claimed all living things.\n\n"My sons," Yanbirde would say, "somewhere in this world there must be a way to defeat Death. This is the greatest quest any hero could undertake."`,
    vocab: [["батыр","hero","ba-TIR"],["тау","mountain","TAU"],["һыу","water","SIU"]],
    memory: { peg: "BIRTH = New BEGINNING on an island", image: "A tiny island after a flood. An elderly couple with silver hair. Two boys — one with dark eyes, one with bright eyes." }},
  { id: 2, title: "The White Swan Maidens", bashkir: "Аҡҡош ҡыҙҙары", icon: Bird, color: "from-sky-800 to-sky-600",
    summary: "The brothers discover swan maidens; Ural shows kindness",
    text: `One day, while hunting far from home, the brothers came upon a crystal lake hidden among the hills. There they witnessed a marvel—seven white swans descended from the sky, transforming into beautiful maidens.\n\nShulgen whispered, "Let us steal their robes! Then they cannot fly away."\n\nBut Ural felt this was wrong. "We should not trap them through trickery."\n\nShulgen seized the robes anyway. Most maidens fled, but the youngest, Humai, could not reach hers. Ural, moved by compassion, returned it to her.\n\nGrateful, Humai told them of kingdoms beyond, of the serpent king Kahkaha, and of the Spring of Life that could grant immortality.`,
    vocab: [["аҡҡош","swan","ak-KOSH"],["күл","lake","KUL"],["ҡыҙ","maiden","KIZ"]],
    memory: { peg: "SWAN = Seven WHITE beauties", image: "Crystal lake. Seven swans become women. One brother grabs robes, the other returns them." }},
  { id: 3, title: "The Quest Begins", bashkir: "Юлға сығыу", icon: Compass, color: "from-blue-900 to-blue-700",
    summary: "Ural seeks the Spring of Life; Shulgen chooses darkness",
    text: `The brothers prepared to leave home. Their father gave Ural a star-metal sword that had never broken.\n\nAt a crossroads, their paths diverged. Ural declared he would seek the Spring of Life to bring immortality to all good creatures.\n\nBut Shulgen had other plans. "Why give life to all? Power lies in controlling life and death. I will seek the serpent king Kahkaha."\n\nUral pleaded with his brother, but Shulgen's heart had already turned. They separated—Ural toward the rising sun, Shulgen toward lands of shadow.`,
    vocab: [["юл","road","YUL"],["ҡылыс","sword","ky-LIS"],["урман","forest","ur-MAN"]],
    memory: { peg: "QUEST = Question of CHOICE", image: "Crossroads at dawn. One path lit by sun, one shrouded in shadow. Two brothers part ways." }},
  { id: 4, title: "The Kingdom of Samrau", bashkir: "Самрау батшалығы", icon: Crown, color: "from-amber-600 to-yellow-500",
    summary: "Ural wins King Samrau's trust and Humai's love",
    text: `After many moons of travel, Ural reached a prosperous kingdom ruled by the wise King Samrau. A shadow had fallen across his realm—creatures from dark lands raided villages.\n\nUral offered his sword and courage. In battle after battle, he proved himself the mightiest warrior the kingdom had ever seen.\n\nKing Samrau was grateful. "Name any reward," he told Ural.\n\nBut Ural had already found his reward—the king's daughter was Humai, the swan maiden he had helped. Love blossomed between them.\n\n"You showed kindness when you could have shown cruelty," she said. "Such a man is worthy of any woman's heart."`,
    vocab: [["батша","king","bat-SHA"],["ил","country","IL"],["йөрәк","heart","yu-RAK"]],
    memory: { peg: "SAMRAU = SAM flew REGAL", image: "Palace above clouds. Giant bird-king on throne. Swan maiden recognizes the kind brother." }},
  { id: 5, title: "The Serpent's Domain", bashkir: "Йылан батшалы", icon: Flame, color: "from-red-900 to-red-700",
    summary: "Shulgen joins Kahkaha and gains dark powers",
    text: `While Ural found love, Shulgen descended into darkness. He found the serpent king Kahkaha in a vast underground realm where no sunlight reached.\n\nKahkaha was ancient beyond measure, a being of scales and venom. "You wish to be mighty?" he asked. "Drink of my venom and become as my son."\n\nShulgen drank. It transformed him, filling him with dark power. His eyes became like a snake's.\n\nKahkaha revealed his plan: "We shall seize the Spring of Life and rule all creation forever."\n\nShulgen agreed eagerly, not knowing his own brother sought the same spring for the opposite purpose.`,
    vocab: [["йылан","serpent","yi-LAN"],["ҡараңғы","darkness","ka-ran-GI"],["ҡан","blood","KAN"]],
    memory: { peg: "SERPENT = SOLD his soul", image: "Dark cave lit by hellfire. Bronze dragon offers cup of venom. Man drinks—eyes turn yellow." }},
  { id: 6, title: "Trials of the Hero", bashkir: "Батырҙың һынауҙары", icon: Shield, color: "from-purple-800 to-purple-600",
    summary: "Ural faces three impossible trials",
    text: `With Humai's guidance, Ural learned the Spring of Life lay beyond three deadly trials.\n\nThe First Trial was the Cave of Riddles. Ural answered truthfully, even when painful.\n\nThe Second Trial was the Plain of Swords—fighting a thousand ghost warriors. For seven days and nights Ural battled without rest.\n\nThe Third Trial was the Test of Sacrifice. Ural came upon a village dying of plague. He could have walked past—the spring was so close!—but he stopped. For months he cared for the sick.\n\nA guardian spirit appeared. "You gave up time for strangers. This is true heroism. Pass, Ural-batyr."`,
    vocab: [["һынау","trial","si-NAU"],["суап","answer","su-AP"],["көс","strength","KUS"]],
    memory: { peg: "TRIALS = THREE tests of TRUTH", image: "Sphinx asking riddles. Battlefield of ghosts. Village of sick people being healed." }},
  { id: 7, title: "War of Light and Darkness", bashkir: "Яҡты һәм ҡараңғы һуғышы", icon: Sword, color: "from-orange-800 to-orange-600",
    summary: "Brother faces brother as Kahkaha's armies attack",
    text: `As Ural climbed the final peak, darkness spread across the lands below. Kahkaha had launched his war.\n\nLeading the vanguard was Shulgen, twisted by dark magic. Brother faced brother on the mountainside.\n\n"Turn back, Shulgen!" Ural pleaded.\n\n"I am more than I ever was!" Shulgen screamed, attacking with serpent-speed.\n\nTheir battle shook the mountain. The fight lasted three days. Finally, Ural landed a terrible blow.\n\nAs Shulgen lay dying, clarity returned to his eyes. "Brother... I see now what I became. Forgive me..."\n\nBut even as Ural wept, Kahkaha himself rose from the shadows.`,
    vocab: [["һуғыш","war","hu-GISH"],["дошман","enemy","dosh-MAN"],["ғәләбә","victory","ga-la-BA"]],
    memory: { peg: "WAR = Brothers WRESTLE fate", image: "Mountain shaking. Two brothers fighting. One falls, asking forgiveness." }},
  { id: 8, title: "The Final Battle", bashkir: "Һуңғы һуғыш", icon: Zap, color: "from-red-800 to-orange-600",
    summary: "Ural defeats Kahkaha through the power of love",
    text: `Kahkaha was primordial evil. His scales deflected Ural's sword. His venom burned like fire.\n\n"I cannot be killed!" Kahkaha laughed. "Kneel, and I may let you live as my slave."\n\nUral remembered Humai's words: "True evil cannot stand true love."\n\nInstead of attacking, Ural began to speak—of his love for Humai, of his parents' kindness, of beauty and hope.\n\nWith each word, Kahkaha writhed as if burned. Love was poison to a being of pure hatred.\n\nUral continued speaking, and as he spoke, he struck. His star-metal sword, glowing with inner light, pierced Kahkaha's heart—for love had revealed where that black heart was hidden.`,
    vocab: [["йән","soul","YAN"],["өмөт","hope","u-MUT"],["мәхәббәт","love","ma-khab-BAT"]],
    memory: { peg: "FINAL = LOVE defeats FEAR", image: "Dragon recoiling from words of love. Glowing sword finds the hidden heart." }},
  { id: 9, title: "The Spring of Life", bashkir: "Тереклек шишмәһе", icon: Droplets, color: "from-cyan-700 to-blue-500",
    summary: "Ural makes an impossible choice",
    text: `Beyond the battlefield, Ural reached the Spring of Life. Its waters glowed with golden light.\n\nA voice spoke: "You may drink and become immortal, living forever in youth and strength."\n\nUral cupped water but did not drink. "Can these waters free everyone from death?"\n\n"They can, but there is a price. You may drink and live forever alone, or pour the waters across the world, granting long life to all—but you yourself will become part of the spring, unable to live among those you save."\n\nUral thought of every person suffering, every mother weeping for a lost child.\n\nHe poured the water.\n\nGolden light spread across the world. Rivers ran cleaner. Crops grew taller. The shadow of death retreated.`,
    vocab: [["тереклек","life","te-rek-LEK"],["шишмә","spring","shish-MA"],["бүләк","gift","bu-LAK"]],
    memory: { peg: "SPRING = SACRIFICE for all", image: "Golden spring on mountaintop. Man pours water outward instead of drinking. Light spreads everywhere." }},
  { id: 10, title: "The Hero's Legacy", bashkir: "Батырҙың мираҫы", icon: Mountain, color: "from-slate-700 to-slate-500",
    summary: "Ural becomes the mountains—living forever through his deeds",
    text: `As the golden waters spread, Ural's body began to change. His legs became mountain roots. His arms became ridges. His heart became crystal deep underground.\n\nHumai flew to him in swan form, tears falling like diamonds.\n\n"Do not weep," Ural said, his voice now rumble of stone and wind. "I am not dying—I am becoming something greater. These mountains will be my body, and I will protect our people forever."\n\nWhere Ural-batyr had stood, there now rose the Ural Mountains—spine of the world, eternal and unbreaking.\n\nThe people who lived in Ural's shadow called themselves Bashkirs—keepers of his memory, children of the mountains.\n\n${LEGACY_PROVERB.bashkir}\n"${LEGACY_PROVERB.english}"\n\nTHE END`,
    vocab: [["тау","mountain","TAU"],["мираҫ","legacy","mi-RAS"],["халыҡ","people","kha-LIK"]],
    memory: { peg: "LEGACY = LOVE becomes LAND", image: "Man transforming into mountain range. Swan singing on highest peak. People gathering in the valleys." }}
];

// ═══════════════════════════════════════════════════════════════════════════════
// VOCABULARY DATA
// ═══════════════════════════════════════════════════════════════════════════════
const vocabCategories = [
  { name: "Greetings", icon: "👋", words: [
    ["һаумыһығыҙ","hello","sau-mih-SIGH-giz"],["һау бул","goodbye","SAU bool"],["рәхмәт","thank you","rakh-MET"],
    ["әйе","yes","AY-eh"],["юҡ","no","YOOK"],["яҡшы","good","yak-SHIH"],["зинһар","please","zin-HAR"]]},
  { name: "Nature", icon: "🏔️", words: [
    ["тау","mountain","TAU"],["йылға","river","yil-GA"],["урман","forest","ur-MAN"],["күл","lake","KUL"],
    ["ер","earth","YER"],["күк","sky","KUK"],["ҡояш","sun","ko-YASH"],["ай","moon","AY"],["һыу","water","SIU"]]},
  { name: "Family", icon: "👨‍👩‍👧‍👦", words: [
    ["атай","father","a-TAY"],["әсәй","mother","a-SAY"],["ул","son","UL"],["ҡыҙ","daughter","KIZ"],
    ["бабай","grandfather","ba-BAY"],["өләсәй","grandmother","o-la-SAY"],["бала","child","ba-LA"]]},
  { name: "Animals", icon: "🐴", words: [
    ["ат","horse","AT"],["бүре","wolf","bu-RE"],["айыу","bear","ay-YU"],["аҡҡош","swan","ak-KOSH"],
    ["бөркөт","eagle","bor-KOT"],["йылан","snake","yi-LAN"],["балыҡ","fish","ba-LIK"]]},
  { name: "Numbers", icon: "🔢", words: [
    ["бер","one","BER"],["ике","two","ee-KE"],["өс","three","OS"],["дүрт","four","DURT"],["биш","five","BISH"],
    ["алты","six","al-TI"],["ете","seven","ye-TE"],["һигеҙ","eight","si-GEZ"],["туғыҙ","nine","tu-GIZ"],["ун","ten","UN"]]},
  { name: "Epic Terms", icon: "⚔️", words: [
    ["батыр","hero","ba-TIR"],["ҡурай","kurai flute","ku-RAY"],["һабантуй","sabantuy","sa-ban-TUY"],
    ["сәсән","bard","sa-SEN"],["тамға","clan symbol","tam-GA"],["йорт","yurt","YORT"]]}
];

// ═══════════════════════════════════════════════════════════════════════════════
// CULTURAL FACTS, PROVERBS, TIMELINE
// ═══════════════════════════════════════════════════════════════════════════════
const culturalFacts = [
  ["history","Ancient Origins","Bashkirs are among the oldest Turkic peoples, with mentions dating back over 1,000 years.","~1000 CE"],
  ["history","Voluntary Union","Bashkir tribes voluntarily joined Russia in 1557, receiving treaty guarantees.","1557"],
  ["history","First Republic","The Bashkir ASSR was formed March 20, 1919—one of the first Soviet autonomous republics.","1919"],
  ["history","Great Famine","The 1921-1922 famine killed over 700,000 Bashkirs—nearly a third of the population.","1921-22"],
  ["history","Salavat Yulaev","National hero (1754-1800) who fought in the Pugachev Rebellion.","1754-1800"],
  ["culture","The Kurai","Traditional wind instrument. UNESCO recognized kurai music in 2010.","Traditional"],
  ["culture","Sabantuy","'Plow festival' with kuresh wrestling and horse racing.","Annual"],
  ["culture","Epic Poetry","The kubair genre performed by sesen bards preserves mythology.","Ancient"],
  ["geography","Ural Mountains","Yamantau (1,640m) and Iremel (1,582m). Legend says these are Ural-Batyr's body.","Geological"],
  ["geography","Agidel River","Main river, 1,430 km. 'White River' in Bashkir.","Geographic"],
  ["geography","Kushtau","Symbol of 2020 environmental victory protecting it from mining.","2020"],
  ["geography","Shulgan-Tash","Cave with 16,000-year-old paintings. Sacred in Ural-Batyr epic.","~14,000 BCE"],
  ["politics","Constitution","Republic within Russia with own constitution (1993) and state languages.","1993"],
  ["politics","Baymak 2024","Large protests after activist Fail Alsynov's sentencing.","2024"],
  ["language","Bashkir","Kipchak Turkic with ~1.2 million speakers. Cyrillic with 9 extra letters.","Linguistic"],
  ["language","UNESCO Status","Classified as 'vulnerable' in 2009.","2009"]
];

const proverbs = [
  ["Legacy", LEGACY_PROVERB.bashkir, LEGACY_PROVERB.russian, LEGACY_PROVERB.english],
  ["Wisdom","Аҡылһыҙ баш асҡҡа аҙап","Глупая голова ногам покоя не даёт","A foolish head gives no rest to the feet"],
  ["Homeland","Ағас тамырынан ныҡлы","Дерево сильно корнями","A tree is strong by its roots"],
  ["Homeland","Тыуған ер — алтын бишек","Родная земля — золотая колыбель","Native land is a golden cradle"],
  ["Heroism","Батыр үлмәй, аты ҡала","Батыр не умирает, имя остаётся","The hero doesn't die, his name remains"],
  ["Unity","Берҙәмлек — көс","Единство — сила","Unity is strength"],
  ["Unity","Халыҡ көсө — таш тишә","Народная сила — камень пробивает","The people's strength pierces stone"],
  ["Nature","Һыу — тереклек сишмәһе","Вода — источник жизни","Water is the spring of life"],
  ["Work","Эш кешене аңрай","Труд человека кормит","Work feeds a person"]
];

const timeline = [
  ["~1000","First written mentions of Bashkirs"],["1557","Voluntary union with Russia"],
  ["1739","Kisyabika Bayryasova executed"],["1773-75","Salavat Yulaev in Pugachev Rebellion"],
  ["1919","Bashkir ASSR formed"],["1921-22","Great Famine"],["1990","Sovereignty declared"],
  ["1993","Constitution adopted"],["2009","UNESCO 'vulnerable' status"],["2020","Kushtau victory"],["2024","Baymak protests"]
];

const twelveReasons = [
  ["Colonial Status","Resources extracted while local interests ignored"],
  ["Indigenous Rights","Bashkirs are indigenous with no other homeland"],
  ["Legal Rights","International law supports self-determination"],
  ["Historical Oppression","Centuries of colonization made Bashkirs a minority"],
  ["Religious Oppression","Muslim majority faces institutional discrimination"],
  ["Language Oppression","Systematic destruction since 2017 policy changes"],
  ["Cultural Oppression","Authentic expression suppressed"],
  ["Replacing Heroes","Genuine heroes replaced with Moscow-serving figures"],
  ["Persecution","Ongoing persecution of political figures"],
  ["Resource Theft","Natural resources extracted for Moscow"],
  ["Assimilation","Large-scale cultural/linguistic assimilation"],
  ["Economic Exploitation","Despite vast resources, remains subordinate"]
];

const mapCities = [
  ["Ufa",50,38,"1.1M","capital"],["Sterlitamak",45,52,"280K","major"],["Salavat",43,56,"155K","city"],
  ["Neftekamsk",42,18,"140K","major"],["Beloretsk",72,52,"66K","city"],["Sibay",75,72,"60K","city"],
  ["Baymak",68,75,"18K","city"],["Oktyabrsky",32,48,"115K","major"],["Birsk",52,28,"45K","city"]
];

const mapLandmarks = [
  ["Mt. Yamantau",75,55,"⛰️","1,640m - Highest peak"],
  ["Mt. Iremel",80,48,"⛰️","1,582m - Sacred mountain"],
  ["Kushtau",44,54,"⛰️","2020 environmental victory"],
  ["Shulgan-Tash",72,62,"🎨","16,000-year-old cave art"]
];

const alphabet = ['А','Б','В','Г','Ғ','Д','Ҙ','Е','Ё','Ж','З','И','Й','К','Ҡ','Л','М','Н','Ң','О','Ө','П','Р','С','Ҫ','Т','У','Ү','Ф','Х','Һ','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ә','Ю','Я'];
const specialLetters = ['Ә','Ө','Ү','Ғ','Ҡ','Ң','Ҙ','Ҫ','Һ'];

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN APPLICATION
// ═══════════════════════════════════════════════════════════════════════════════
const GoldenLightApp = () => {
  const [view, setView] = useState('home');
  const [expandedChapter, setExpandedChapter] = useState(null);
  const [chapter, setChapter] = useState(0);
  const [vocabCat, setVocabCat] = useState(0);
  const [factFilter, setFactFilter] = useState('all');
  const [proverbFilter, setProverbFilter] = useState('all');
  const [docTab, setDocTab] = useState('12reasons');
  const [mapFilter, setMapFilter] = useState('all');
  const [selectedLoc, setSelectedLoc] = useState(null);
  const [flashIdx, setFlashIdx] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);

  const allVocab = vocabCategories.flatMap(c => c.words.map(w => ({ cat: c.name, w })));
  const navTabs = [
    { id: 'home', icon: Home, label: 'Home' },
    { id: 'epic', icon: Scroll, label: 'Epic' },
    { id: 'palace', icon: Compass, label: 'Palace' },
    { id: 'vocab', icon: Languages, label: 'Vocab' },
    { id: 'map', icon: Map, label: 'Map' },
    { id: 'documents', icon: FileText, label: 'Docs' },
    { id: 'facts', icon: Lightbulb, label: 'Facts' },
    { id: 'proverbs', icon: Quote, label: 'Proverbs' },
    { id: 'timeline', icon: History, label: 'History' },
    { id: 'alphabet', icon: BookOpen, label: 'Letters' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <header className="bg-gradient-to-r from-amber-700 via-orange-600 to-amber-700 p-4 shadow-xl">
        <div className="max-w-6xl mx-auto flex items-center gap-3">
          <Sun className="w-10 h-10 text-yellow-300" />
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold">Алтын Яҡты — Golden Light</h1>
            <p className="text-amber-100 text-xs sm:text-sm">The Legacy Edition · v1.3.1</p>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-slate-800/90 backdrop-blur border-b border-slate-700 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto flex overflow-x-auto">
          {navTabs.map(tab => (
            <button key={tab.id} onClick={() => setView(tab.id)}
              className={`flex-1 min-w-max py-2 px-2 text-xs font-medium transition-all flex flex-col items-center gap-0.5 ${
                view === tab.id ? 'bg-amber-600/30 text-amber-400 border-b-2 border-amber-400' : 'text-slate-400 hover:text-white'}`}>
              <tab.icon className="w-4 h-4" /><span>{tab.label}</span>
            </button>
          ))}
        </div>
      </nav>

      <main className="max-w-6xl mx-auto p-4">
        {/* ═══════════════════════════════════════════════════════════════ HOME */}
        {view === 'home' && (
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-amber-900/40 via-orange-800/30 to-slate-800 rounded-2xl p-6 border border-amber-700/50 text-center">
              <Sun className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
              <h2 className="text-3xl font-bold text-amber-400">Welcome to Golden Light</h2>
              <p className="text-slate-300 mt-2">Башҡорт мәҙәниәтенә һәм телгә юл — A path to Bashkir culture and language</p>
            </div>

            {/* Legacy Proverb Banner */}
            <div className="bg-gradient-to-r from-amber-900/60 to-amber-800/40 rounded-xl p-5 border-2 border-amber-500/50">
              <p className="text-xl font-bold text-amber-300 text-center">"{LEGACY_PROVERB.bashkir}"</p>
              <p className="text-amber-100/80 text-center mt-2 italic">{LEGACY_PROVERB.english}</p>
              <p className="text-amber-400/60 text-center text-xs mt-1">[{LEGACY_PROVERB.phonetic}]</p>
            </div>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { v: 'epic', icon: Scroll, title: 'Ural-Batyr Epic', desc: '10 chapters of heroic legend', color: 'from-purple-700 to-purple-500' },
                { v: 'palace', icon: Compass, title: 'Memory Palace', desc: 'Learn through story stations', color: 'from-blue-700 to-blue-500' },
                { v: 'map', icon: Map, title: 'Interactive Map', desc: 'Cities, towns, landmarks', color: 'from-emerald-700 to-emerald-500' },
                { v: 'vocab', icon: Languages, title: 'Flashcards', desc: '6 categories, 50+ words', color: 'from-cyan-700 to-cyan-500' },
                { v: 'documents', icon: FileText, title: 'Documents', desc: '12 Reasons, Salavat bio', color: 'from-amber-700 to-amber-500' },
                { v: 'facts', icon: Lightbulb, title: 'Cultural Facts', desc: 'History, geography, culture', color: 'from-pink-700 to-pink-500' }
              ].map(item => (
                <button key={item.v} onClick={() => setView(item.v)}
                  className={`bg-gradient-to-br ${item.color} rounded-xl p-5 text-left hover:scale-105 transition-transform`}>
                  <item.icon className="w-8 h-8 mb-2" />
                  <h3 className="font-bold text-lg">{item.title}</h3>
                  <p className="text-white/70 text-sm">{item.desc}</p>
                </button>
              ))}
            </div>

            <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
              <h3 className="font-bold text-amber-400 mb-3">✨ v1.3.1 — The Legacy Edition</h3>
              <p className="text-slate-300 text-sm">Anchored by the proverb: "{LEGACY_PROVERB.english}" — reflecting Ural-Batyr's sacrifice and the enduring Bashkir spirit.</p>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ EPIC */}
        {view === 'epic' && (
          <div className="space-y-4">
            <div className="bg-gradient-to-r from-amber-900/40 to-slate-800 rounded-xl p-6 border border-amber-700/50">
              <h2 className="text-2xl font-bold text-amber-400">Урал-Батыр / Ural-Batyr</h2>
              <p className="text-slate-300">Башҡорт халыҡ эпосы • 4,576 lines • The foundational myth</p>
            </div>
            {epicChapters.map((ch, idx) => (
              <div key={ch.id} className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
                <button onClick={() => setExpandedChapter(expandedChapter === idx ? null : idx)}
                  className="w-full p-4 flex items-center gap-4 hover:bg-slate-700/50">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${ch.color} flex items-center justify-center flex-shrink-0`}>
                    <ch.icon className="w-6 h-6" />
                  </div>
                  <div className="flex-1 text-left">
                    <p className="font-bold">Ch. {ch.id}: {ch.title}</p>
                    <p className="text-xs text-amber-400">{ch.bashkir}</p>
                    <p className="text-sm text-slate-400 line-clamp-1">{ch.summary}</p>
                  </div>
                  <ChevronDown className={`w-5 h-5 transition-transform flex-shrink-0 ${expandedChapter === idx ? 'rotate-180' : ''}`} />
                </button>
                {expandedChapter === idx && (
                  <div className="p-4 border-t border-slate-700 space-y-4">
                    <p className="text-slate-300 whitespace-pre-line text-sm leading-relaxed">{ch.text}</p>
                    <div className="bg-purple-900/30 rounded-lg p-4 border border-purple-700/50">
                      <p className="text-purple-400 font-bold mb-2">🧠 Memory Technique</p>
                      <p className="text-sm font-mono text-white">{ch.memory.peg}</p>
                      <p className="text-sm text-slate-300 mt-1">{ch.memory.image}</p>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      {ch.vocab.map(([b,e,p], i) => (
                        <div key={i} className="bg-slate-700/50 rounded-lg p-2 text-center">
                          <p className="text-amber-400 font-bold">{b}</p>
                          <p className="text-xs text-slate-400">[{p}]</p>
                          <p className="text-xs text-slate-300">{e}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ PALACE */}
        {view === 'palace' && (
          <div className="space-y-4">
            <div className="flex gap-1 overflow-x-auto pb-2">
              {epicChapters.map((ch, idx) => (
                <button key={idx} onClick={() => setChapter(idx)}
                  className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center ${
                    chapter === idx ? `bg-gradient-to-br ${ch.color} ring-2 ring-amber-400` : 'bg-slate-700 hover:bg-slate-600'}`}>
                  <ch.icon className="w-5 h-5" />
                </button>
              ))}
            </div>
            <div className={`bg-gradient-to-br ${epicChapters[chapter].color} rounded-xl p-6`}>
              <p className="text-white/70 text-sm">Station {chapter + 1} of 10</p>
              <h3 className="text-2xl font-bold">{epicChapters[chapter].title}</h3>
              <p className="text-white/80">{epicChapters[chapter].bashkir}</p>
            </div>
            <div className="bg-purple-900/30 rounded-xl p-5 border border-purple-700/50">
              <h4 className="font-bold text-purple-400 mb-3">🧠 Method of Loci</h4>
              <p className="text-lg font-mono text-white">{epicChapters[chapter].memory.peg}</p>
              <p className="text-slate-300 mt-2">{epicChapters[chapter].memory.image}</p>
            </div>
            <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
              <h4 className="font-bold text-amber-400 mb-3">Station Vocabulary</h4>
              <div className="grid grid-cols-3 gap-3">
                {epicChapters[chapter].vocab.map(([b,e,p], i) => (
                  <div key={i} className="bg-slate-700/50 rounded-lg p-3">
                    <p className="text-xl font-bold text-amber-400">{b}</p>
                    <p className="text-xs text-slate-400">[{p}]</p>
                    <p className="text-slate-300">{e}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="flex justify-between">
              <button onClick={() => setChapter(Math.max(0, chapter - 1))} disabled={chapter === 0}
                className="px-4 py-2 bg-slate-700 rounded-lg disabled:opacity-50 flex items-center gap-2">
                <ChevronLeft className="w-4 h-4" /> Previous
              </button>
              <button onClick={() => setChapter(Math.min(9, chapter + 1))} disabled={chapter === 9}
                className="px-4 py-2 bg-slate-700 rounded-lg disabled:opacity-50 flex items-center gap-2">
                Next <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ VOCAB */}
        {view === 'vocab' && (
          <div className="space-y-4">
            <div className="flex gap-2 flex-wrap">
              {vocabCategories.map((c, i) => (
                <button key={i} onClick={() => setVocabCat(i)}
                  className={`px-3 py-1 rounded-lg text-sm ${vocabCat === i ? 'bg-amber-500 text-white' : 'bg-slate-700'}`}>
                  {c.icon} {c.name}
                </button>
              ))}
            </div>
            <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
              <h3 className="font-bold text-amber-400 mb-4">{vocabCategories[vocabCat].icon} {vocabCategories[vocabCat].name}</h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {vocabCategories[vocabCat].words.map(([b,e,p], i) => (
                  <div key={i} className="bg-slate-700/50 rounded-lg p-3 text-center">
                    <p className="text-xl font-bold text-amber-400">{b}</p>
                    <p className="text-xs text-slate-400">[{p}]</p>
                    <p className="text-slate-300">{e}</p>
                  </div>
                ))}
              </div>
            </div>
            {/* Flashcard Mode */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border-2 border-amber-500/50 text-center cursor-pointer"
              onClick={() => setShowAnswer(!showAnswer)}>
              <p className="text-slate-400 text-sm mb-2">{allVocab[flashIdx].cat} • Card {flashIdx + 1}/{allVocab.length}</p>
              {!showAnswer ? (
                <>
                  <p className="text-4xl font-bold text-amber-400 mb-2">{allVocab[flashIdx].w[0]}</p>
                  <p className="text-slate-400">Tap to reveal</p>
                </>
              ) : (
                <>
                  <p className="text-2xl text-white mb-1">{allVocab[flashIdx].w[1]}</p>
                  <p className="text-amber-300">[{allVocab[flashIdx].w[2]}]</p>
                </>
              )}
            </div>
            <div className="flex justify-center gap-4">
              <button onClick={() => { setFlashIdx((flashIdx - 1 + allVocab.length) % allVocab.length); setShowAnswer(false); }}
                className="px-4 py-2 bg-slate-700 rounded-lg">← Prev</button>
              <button onClick={() => { setFlashIdx((flashIdx + 1) % allVocab.length); setShowAnswer(false); }}
                className="px-4 py-2 bg-slate-700 rounded-lg">Next →</button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ MAP */}
        {view === 'map' && (
          <div className="space-y-4">
            <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
              <h2 className="text-xl font-bold">Republic of Bashkortostan</h2>
              <p className="text-slate-400 text-sm">Башҡортостан Республикаһы • 143,600 km² • 4 million people</p>
            </div>
            <div className="flex gap-2 flex-wrap">
              {['all', 'cities', 'landmarks'].map(f => (
                <button key={f} onClick={() => setMapFilter(f)}
                  className={`px-3 py-1 rounded-lg text-sm ${mapFilter === f ? 'bg-amber-500 text-white' : 'bg-slate-700'}`}>
                  {f.charAt(0).toUpperCase() + f.slice(1)}
                </button>
              ))}
            </div>
            <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
              <div className="relative w-full" style={{ paddingBottom: '90%' }}>
                <svg viewBox="0 0 100 100" className="absolute inset-0 w-full h-full">
                  <defs>
                    <linearGradient id="landGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#334155" /><stop offset="100%" stopColor="#1e293b" />
                    </linearGradient>
                  </defs>
                  <path d="M12,18 Q8,35 12,55 Q15,70 25,82 Q40,92 55,88 Q75,82 88,65 Q95,45 90,25 Q82,12 65,8 Q45,5 30,8 Q18,12 12,18" fill="url(#landGrad)" stroke="#64748b" strokeWidth="0.5" />
                  <path d="M70,5 Q75,20 78,35 Q82,50 80,65 Q78,80 75,95" fill="none" stroke="#64748b" strokeWidth="8" strokeLinecap="round" opacity="0.3" />
                  <path d="M80,42 Q72,45 60,38 Q52,35 50,32 Q45,35 38,45 Q32,55 28,70" fill="none" stroke="#38bdf8" strokeWidth="1" opacity="0.7" />
                  <text x="35" y="72" fill="#38bdf8" fontSize="2">Ағиҙел</text>
                  {(mapFilter === 'all' || mapFilter === 'cities') && mapCities.map(([name,x,y,pop,type], i) => (
                    <g key={i} onClick={() => setSelectedLoc({ name, pop, type: 'city' })} className="cursor-pointer">
                      <circle cx={x} cy={y} r={type === 'capital' ? 2.5 : type === 'major' ? 1.8 : 1.2}
                        fill={type === 'capital' ? '#f59e0b' : '#ef4444'} stroke="#fff" strokeWidth="0.3" />
                      {(type === 'capital' || type === 'major') && <text x={x + 3} y={y + 1} fill="#e2e8f0" fontSize="2.2">{name}</text>}
                    </g>
                  ))}
                  {(mapFilter === 'all' || mapFilter === 'landmarks') && mapLandmarks.map(([name,x,y,icon,desc], i) => (
                    <g key={i} onClick={() => setSelectedLoc({ name, desc, type: 'landmark' })} className="cursor-pointer">
                      <text x={x} y={y} fontSize="4" textAnchor="middle">{icon}</text>
                    </g>
                  ))}
                </svg>
              </div>
            </div>
            {selectedLoc && (
              <div className="bg-slate-800 rounded-xl p-4 border border-amber-500">
                <h3 className="font-bold text-amber-400">{selectedLoc.name}</h3>
                <p className="text-slate-300 text-sm">{selectedLoc.pop || selectedLoc.desc}</p>
                <button onClick={() => setSelectedLoc(null)} className="mt-2 text-xs text-slate-400">Clear selection</button>
              </div>
            )}
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ DOCUMENTS */}
        {view === 'documents' && (
          <div className="space-y-4">
            <div className="flex gap-2">
              {[['12reasons', '12 Reasons'], ['salavat', 'Salavat Yulaev']].map(([id, label]) => (
                <button key={id} onClick={() => setDocTab(id)}
                  className={`px-4 py-2 rounded-lg ${docTab === id ? 'bg-amber-500' : 'bg-slate-700'}`}>{label}</button>
              ))}
            </div>
            {docTab === '12reasons' && (
              <div className="space-y-3">
                <div className="bg-amber-900/30 rounded-xl p-4 border border-amber-700/50">
                  <h2 className="text-xl font-bold text-amber-400">12 Reasons Why Bashkirs Must Attain Independence</h2>
                  <p className="text-slate-400 text-sm">By Ruslan Gabbasov • Free Nations League</p>
                </div>
                {twelveReasons.map(([title, desc], i) => (
                  <div key={i} className="bg-slate-800 rounded-lg p-4 border border-slate-700">
                    <p className="font-bold text-amber-400">#{i + 1}: {title}</p>
                    <p className="text-slate-300 text-sm">{desc}</p>
                  </div>
                ))}
              </div>
            )}
            {docTab === 'salavat' && (
              <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
                <h2 className="text-2xl font-bold text-amber-400 text-center">Salavat Yulaev</h2>
                <p className="text-amber-300 text-center">Салауат Юлаев • 1754-1800</p>
                <p className="text-slate-300 mt-4 leading-relaxed">National hero, poet, and military leader who fought alongside Yemelyan Pugachev in the 1773-1775 uprising. Born in Tekeyevo village, he proved himself an outstanding commander leading Bashkir cavalry.</p>
                <p className="text-slate-300 mt-3 leading-relaxed">After the rebellion's defeat, he was captured, tortured, branded, and sentenced to eternal hard labor, dying in Baltic exile in 1800. Beyond military achievements, Salavat was a gifted poet expressing love for homeland.</p>
                <div className="mt-4 bg-amber-900/20 rounded-lg p-4 border border-amber-700/50">
                  <p className="text-amber-400 font-bold mb-2">Famous Quotes:</p>
                  <p className="text-slate-300 italic">"My people! I call you to freedom!"</p>
                  <p className="text-slate-300 italic">"The Urals are my father, the steppe is my mother"</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ FACTS */}
        {view === 'facts' && (
          <div className="space-y-4">
            <div className="flex gap-2 flex-wrap">
              {['all', 'history', 'culture', 'geography', 'politics', 'language'].map(f => (
                <button key={f} onClick={() => setFactFilter(f)}
                  className={`px-3 py-1 rounded-lg text-sm ${factFilter === f ? 'bg-amber-500 text-white' : 'bg-slate-700'}`}>
                  {f === 'all' ? 'All' : f.charAt(0).toUpperCase() + f.slice(1)}
                </button>
              ))}
            </div>
            <div className="space-y-3">
              {culturalFacts.filter(([cat]) => factFilter === 'all' || cat === factFilter).map(([cat, title, content, year], i) => (
                <div key={i} className="bg-slate-800 rounded-lg p-4 border border-slate-700">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs bg-amber-500/20 text-amber-400 px-2 py-1 rounded">{cat}</span>
                    <span className="text-xs text-slate-500">{year}</span>
                  </div>
                  <h4 className="font-bold text-white">{title}</h4>
                  <p className="text-slate-300 text-sm">{content}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ PROVERBS */}
        {view === 'proverbs' && (
          <div className="space-y-4">
            <div className="flex gap-2 flex-wrap">
              {['all', ...new Set(proverbs.map(p => p[0]))].map(f => (
                <button key={f} onClick={() => setProverbFilter(f)}
                  className={`px-3 py-1 rounded-lg text-sm ${proverbFilter === f ? 'bg-amber-500' : 'bg-slate-700'}`}>
                  {f === 'all' ? 'All' : f}
                </button>
              ))}
            </div>
            {proverbs.filter(([cat]) => proverbFilter === 'all' || cat === proverbFilter).map(([cat, b, r, e], i) => (
              <div key={i} className="bg-slate-800 rounded-xl p-4 border border-slate-700 border-l-4 border-l-amber-500">
                <span className="text-xs bg-amber-500/20 text-amber-400 px-2 py-1 rounded">{cat}</span>
                <p className="text-xl font-bold text-amber-400 mt-3">{b}</p>
                <p className="text-slate-400 text-sm mt-1">🇷🇺 {r}</p>
                <p className="text-slate-300 mt-1">🇬🇧 {e}</p>
              </div>
            ))}
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ TIMELINE */}
        {view === 'timeline' && (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-amber-400">Historical Timeline</h2>
            <div className="relative pl-8 space-y-4">
              <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-gradient-to-b from-amber-500 via-amber-600 to-amber-700" />
              {timeline.map(([year, event], i) => (
                <div key={i} className="relative">
                  <div className="absolute left-[-22px] w-4 h-4 rounded-full bg-amber-500 border-2 border-slate-900" />
                  <div className="bg-slate-800 rounded-lg p-3 border border-slate-700">
                    <span className="text-amber-400 font-bold">{year}</span>
                    <p className="text-slate-300 text-sm">{event}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ ALPHABET */}
        {view === 'alphabet' && (
          <div className="space-y-4">
            <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
              <h2 className="text-xl font-bold text-amber-400">The Bashkir Alphabet</h2>
              <p className="text-slate-400 text-sm">42 letters based on Cyrillic, including 9 unique to Bashkir</p>
            </div>
            <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
              <h3 className="font-bold text-amber-400 mb-3">Nine Special Letters</h3>
              <div className="flex flex-wrap gap-2 justify-center">
                {specialLetters.map((l, i) => (
                  <div key={i} className="w-14 h-14 bg-gradient-to-br from-amber-600 to-amber-500 rounded-xl flex items-center justify-center text-2xl font-bold">{l}</div>
                ))}
              </div>
            </div>
            <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
              <h3 className="font-bold text-amber-400 mb-3">Full Alphabet</h3>
              <div className="flex flex-wrap gap-1 justify-center">
                {alphabet.map((l, i) => (
                  <div key={i} className={`w-9 h-9 rounded-lg flex items-center justify-center text-lg font-bold ${
                    specialLetters.includes(l) ? 'bg-amber-500 text-white' : 'bg-slate-700 text-slate-300'}`}>{l}</div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-700 p-6 mt-8 text-center">
        <p className="text-amber-400 font-bold">"{LEGACY_PROVERB.bashkir}"</p>
        <p className="text-slate-400 text-sm mt-1 italic">{LEGACY_PROVERB.english}</p>
        <p className="text-slate-500 text-xs mt-3">🌄 Golden Light v1.3.1 • Preserving Bashkir heritage through good deeds</p>
      </footer>
    </div>
  );
};

export default GoldenLightApp;
