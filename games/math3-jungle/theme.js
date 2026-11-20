// acc: the accessory an animal wears from its second copy on (crown / neck = necklace with a pendant / bow)
const ITEMS = [
  { id: 'lion', name: 'אריה', icon: '🦁', price: 15, acc: 'crown' },
  { id: 'elephant', name: 'פיל', icon: '🐘', price: 15, acc: 'neck' },
  { id: 'leopard', name: 'נמר', icon: '🐆', price: 20, acc: 'bow' },
  { id: 'giraffe', g: 'f', name: 'ג\'ירפה', icon: '🦒', price: 25, acc: 'neck' },
  { id: 'monkey', name: 'קוף', icon: '🐒', price: 10, acc: 'neck' },
  { id: 'parrot', name: 'תוכי', icon: '🦜', price: 10, acc: 'crown' },
  { id: 'zebra', g: 'f', name: 'זברה', icon: '🦓', price: 10, acc: 'bow' },
  { id: 'koala', g: 'f', name: 'קואלה', icon: '🐨', price: 20, acc: 'crown' },
  { id: 'frog', g: 'f', name: 'צפרדע', icon: '🐸', price: 8, acc: 'bow' },
  { id: 'croc', name: 'תנין', icon: '🐊', price: 20, acc: 'crown' }
];

const GEAR = [
  { id: 'boots', g: 'p', name: 'מגפי טיול', icon: '🥾', r: 0 }, { id: 'hat', name: 'כובע ספארי', icon: '🧢', r: 0 },
  { id: 'bag', name: 'תרמיל', icon: '🎒', r: 0 }, { id: 'tent', name: 'אוהל', icon: '⛺', r: 0 },
  { id: 'shell', name: 'צדף קסום', icon: '🐚', r: 0 }, { id: 'feather', g: 'f', name: 'נוצת תוכי', icon: '🪶', r: 0 },
  { id: 'torch', name: 'פנס', icon: '🔦', r: 1 }, { id: 'map', g: 'f', name: 'מפת אוצר', icon: '🗺️', r: 1 },
  { id: 'compass', name: 'מצפן', icon: '🧭', r: 1 }, { id: 'scope', g: 'f', name: 'משקפת', icon: '🔭', r: 1 },
  { id: 'beads', g: 'f', name: 'שרשרת חרוזים', icon: '📿', r: 1 }, { id: 'eye', name: 'קמע עין', icon: '🧿', r: 1 },
  { id: 'gem', name: 'יהלום הג\'ונגל', icon: '💎', r: 2 }, { id: 'trident', name: 'קלשון הזהב', icon: '🔱', r: 2 },
  { id: 'star', name: 'כוכב המזל', icon: '🌟', r: 2 }, { id: 'crown', name: 'כתר המלך', icon: '👑', r: 2 }
];
const RARITY = ['רגיל', 'נדיר', 'אגדי'];