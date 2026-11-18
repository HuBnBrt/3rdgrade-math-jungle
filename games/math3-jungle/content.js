/* ---------- question generators ---------- */
function genDigit(t) {
  const len = t === 1 ? 3 : 4;
  let n, s;
  do { n = len === 3 ? rnd(100, 999) : rnd(1000, 9999); s = String(n); } while (![...s].some(ch => s.split(ch).length === 2));
  let i, old, e;
  do { i = rnd(0, len - 1); old = Number(s[i]); e = rnd(0, 9); }
  while (e === old || (i === 0 && e === 0) || s.split(String(old)).length !== 2);
  const pv = 10 ** (len - 1 - i);
  const diff = (e - old) * pv;
  if (Math.random() < .4) {
    const nn = n + diff;
    return {
      body: `<div class="prompt">במספר <span class="ltr">${fmt(n)}</span> משנים את ספרת ${PLACE[pv]} ל-${e}.<br>מה המספר החדש?</div>`,
      parts: [{ type: 'num', ans: nn }],
      hint: `ספרת ${PLACE[pv]} היא הספרה ${old}. מחליפים אותה ב-${e} ושאר הספרות נשארות.`,
      explain: `<span class="ltr">${fmt(n)}</span> הופך ל-<span class="ltr">${fmt(nn)}</span>.`
    };
  }
  const amount = Math.abs(diff), grows = diff > 0;
  return {
    body: `<div class="prompt">במספר <span class="ltr">${fmt(n)}</span> שונתה הספרה ${old} ל-${e}.<br>האם המספר החדש גדל או קטן, ובכמה?</div>`,
    parts: [
      { type: 'buttons', opts: ['גדל', 'קטן'], ans: grows ? 'גדל' : 'קטן' },
      { type: 'num', label: 'בכמה', ans: amount }
    ],
    hint: 'כדאי לשים לב לאיזה מקום שייכת הספרה. ההפרש מוכפל בערך המקום.',
    explain: `הספרה ${old} נמצאת במקום ${PLACE[pv]}. לכן המספר ${grows ? 'גדל' : 'קטן'} ב-${fmt(amount)}.`
  };
}

function genCompare(t) {
  const R = t === 1 ? 60 : t === 2 ? 500 : 5000;
  let L, Rt, lv, rv;
  if (Math.random() < .5) {
    const a = rnd(1, R), b = rnd(1, R), c = rnd(1, R), d = rnd(1, R);
    L = `${fmt(a)} + ${fmt(b)}`; Rt = `${fmt(c)} + ${fmt(d)}`; lv = a + b; rv = c + d;
  } else {
    const b = rnd(1, R), a = b + rnd(0, R), c = rnd(1, R), d = c + rnd(0, R);
    L = `${fmt(a)} − ${fmt(b)}`; Rt = `${fmt(d)} − ${fmt(c)}`; lv = a - b; rv = d - c;
  }
  const sym = lv < rv ? '<' : lv > rv ? '>' : '=';
  return {
    body: `<div class="prompt">יש לסמן את הסימן המתאים:</div><div class="prompt" style="font-size:28px"><span class="ltr">${L} &nbsp; ? &nbsp; ${Rt}</span></div>`,
    parts: [{ type: 'buttons', opts: ['>', '=', '<'], ans: sym }],
    hint: 'יש לחשב את שני הצדדים, ואז להשוות את התוצאות.',
    explain: `<span class="ltr">${fmt(lv)} ${sym==='<'?'&lt;':sym==='>'?'&gt;':'='} ${fmt(rv)}</span>`
  };
}

function genNoCalc(t) {
  const R = t === 1 ? 90 : t === 2 ? 900 : 9000;
  const kind = pick(['sameA', 'sameB', 'addSame']);
  let L, Rt, lv, rv, hint;
  if (kind === 'sameA') {
    const b = rnd(1, R), c = rnd(1, R), A = Math.max(b, c) + rnd(0, R);
    L = `${fmt(A)} − ${fmt(b)}`; Rt = `${fmt(A)} − ${fmt(c)}`; lv = A - b; rv = A - c;
    hint = 'המספר הראשון זהה. כשמחסירים מספר גדול יותר, מתקבלת תוצאה קטנה יותר.';
  } else if (kind === 'sameB') {
    const B = rnd(1, R), A = B + rnd(0, R), C = B + rnd(0, R);
    L = `${fmt(A)} − ${fmt(B)}`; Rt = `${fmt(C)} − ${fmt(B)}`; lv = A - B; rv = C - B;
    hint = 'המספר שמחסירים זהה. ככל שהמספר הראשון גדול יותר, התוצאה גדולה יותר.';
  } else {
    const A = rnd(1, R), b = rnd(1, R), c = rnd(1, R);
    L = `${fmt(A)} + ${fmt(b)}`; Rt = `${fmt(A)} + ${fmt(c)}`; lv = A + b; rv = A + c;
    hint = 'המספר הראשון זהה. ככל שמוסיפים מספר גדול יותר, התוצאה גדולה יותר.';
  }
  const sym = lv < rv ? '<' : lv > rv ? '>' : '=';
  return {
    body: `<div class="prompt">יש לסמן ללא צורך בחישוב מדויק:</div><div class="prompt" style="font-size:28px"><span class="ltr">${L} &nbsp; ? &nbsp; ${Rt}</span></div>`,
    parts: [{ type: 'buttons', opts: ['>', '=', '<'], ans: sym }],
    hint,
    explain: `הסימן המתאים הוא <span class="ltr">${sym==='<'?'&lt;':sym==='>'?'&gt;':'='}</span>.`
  };
}

function genDecomp(t) {
  const len = t === 1 ? 3 : 4;
  const n = len === 3 ? rnd(100, 999) : rnd(1000, 9999);
  const comps = String(n).split('').map((x, i) => Number(x) * 10 ** (len - 1 - i));
  const m = rnd(0, len - 1);
  const shown = comps.map((c, j) => j === m ? '___' : fmt(c)).join(' + ');
  return {
    body: `<div class="prompt">יש להשלים את הפירוק:<br><span class="ltr">${fmt(n)} = ${shown}</span></div>`,
    parts: [{ type: 'num', ans: comps[m] }],
    hint: 'כל ספרה שווה לערך שלה לפי המקום.',
    explain: (() => {
      const given = comps.filter((c, j) => j !== m).map(fmt);
      const givenTxt = given.length > 1 ? given.slice(0, -1).join(', ') + ' ו-' + given[given.length - 1] : given[0];
      const place = 10 ** (len - 1 - m), digit = comps[m] / place;
      const UN = { 1: 'יחידות', 10: 'עשרות', 100: 'מאות', 1000: 'אלפים' };
      if (digit === 0) return `כבר יש ${givenTxt}, ולכן החסר הוא 0: אין ${UN[place]} במספר. הפירוק המלא: <span class="ltr">${fmt(n)} = ${comps.filter(c => c).map(fmt).join(' + ')}</span>`;
      return `כבר יש ${givenTxt}, ולכן החסר הוא ${fmt(comps[m])}: הספרה ${digit} נמצאת במקום ${PLACE[place]} ושווה ${fmt(comps[m])}. הפירוק המלא: <span class="ltr">${fmt(n)} = ${comps.map(fmt).join(' + ')}</span>`;
    })()
  };
}

function genOrder(t) {
  const R = t === 1 ? 999 : t === 2 ? 3000 : 9999;
  const set = new Set();
  while (set.size < 5) set.add(rnd(10, R));
  const nums = [...set];
  const sorted = [...nums].sort((x, y) => x - y);
  return {
    body: `<div class="prompt">יש ללחוץ או לגרור את המספרים מהקטן לגדול.</div>`,
    parts: [{ type: 'order', items: shuffle(nums), ans: sorted }],
    hint: 'מומלץ להשוות קודם את מספר הספרות, ואז את הספרות השמאליות ביותר.',
    explain: `הסדר הנכון: <span class="ltr">${sorted.map(fmt).join(' &lt; ')}</span>`
  };
}

function genNumLine(t) {
  const base = t === 1 ? 100 : t === 2 ? 1000 : 3000;
  const a = rnd(base / 10, base / 10 + 80) * 10;
  const b = a + 100;
  const inside = a + rnd(1, 99);
  const outs = new Set();
  while (outs.size < 3) { const x = Math.random() < .5 ? a - rnd(5, 70) : b + rnd(5, 70); if (x > 0) outs.add(x); }
  const opts = shuffle([inside, ...outs]).map(fmt);
  return {
    body: `<div class="prompt">המספרים <span class="ltr">${fmt(a)}</span> ו-<span class="ltr">${fmt(b)}</span> הם קצוות הקטע.<br>איזה מספר נמצא בתוך הקטע?</div>`,
    parts: [{ type: 'buttons', opts, ans: fmt(inside) }],
    hint: 'המספר צריך להיות גדול מהמספר הקטן וקטן מהמספר הגדול.',
    explain: `${fmt(inside)} נמצא בין ${fmt(a)} ל-${fmt(b)}.`
  };
}

function genSeq(t) {
  const k = pick([[1, 2, 5, 10], [10, 20, 50, 100], [100, 200, 500, 1000]][t - 1]);
  const desc = Math.random() < .3;
  const s = desc
    ? k * rnd(7, Math.max(7, Math.min(60, Math.floor(9999 / k))))
    : k * rnd(2, Math.max(2, Math.min(60, Math.floor(9000 / k) - 6)));
  const terms = [0, 1, 2, 3, 4, 5].map(i => s + (desc ? -i : i) * k);
  const blanks = pick([[1, 3], [2, 4], [1, 4]]);
  const sortedBlanks = [...blanks].sort((x, y) => x - y);
  const shown = terms.map((v, i) => blanks.includes(i) ? `<span class="gap">חסר ${sortedBlanks.indexOf(i) + 1}</span>` : fmt(v)).join(', ');
  return {
    body: `<div class="prompt">יש להשלים את הסדרה, שממשיכה בקפיצות של ${fmt(k)}:<br><span class="ltr" style="font-size:28px;margin-top:10px">${shown}</span></div>`,
    parts: sortedBlanks.map((bi, j) => ({ type: 'num', label: `חסר ${j + 1}`, ans: terms[bi] })),
    hint: `בכל שלב יש קפיצה קבועה של ${fmt(k)}.`,
    explain: `הסדרה המלאה: ${terms.map(fmt).join(', ')}`
  };
}

function genSeqMember(t) {
  const k = pick([[2, 5, 10], [10, 20, 50], [100, 200, 500]][t - 1]);
  const s = k * rnd(2, Math.max(2, Math.min(60, Math.floor(9000 / k) - 10)));
  const shown = [0, 1, 2, 3].map(i => fmt(s + i * k)).join(', ');
  const m = rnd(6, 30);
  const yes = Math.random() < .5;
  const X = yes ? s + m * k : s + m * k + rnd(1, k - 1);
  const isIn = (X - s) % k === 0;
  return {
    body: `<div class="prompt">סדרה: <span class="ltr">${shown}, ...</span><br>האם המספר <span class="ltr" style="font-size:32px">${fmt(X)}</span> יופיע בהמשך הסדרה?</div>`,
    parts: [{ type: 'buttons', opts: ['כן', 'לא'], ans: isIn ? 'כן' : 'לא' }],
    hint: 'יש לבדוק אם ההפרש בין המספר המבוקש למספר הראשון מתחלק בקפיצה.',
    explain: `המספר ${isIn ? 'אכן יופיע' : 'לא יופיע'} כי הוא ${isIn ? 'מתחלק' : 'לא מתחלק'} בקפיצות של ${fmt(k)}.`
  };
}

function genSameDigits(t) {
  const len = t === 1 ? 3 : 4;
  const odd = Math.random() < .5, smaller = Math.random() < .6;
  const pw = odd ? 'אי-זוגי' : 'זוגי', dw = smaller ? 'הקטן' : 'הגדול';
  let n, valid = [];
  for (;;) {
    n = len === 3 ? rnd(200, 999) : rnd(2000, 9999);
    const d = String(n).split('');
    if (new Set(d).size !== len) continue;
    valid = [...new Set(perms(d).filter(x => x[0] !== '0').map(x => Number(x.join(''))).filter(v => (smaller ? v < n : v > n) && (v % 2 === 1) === odd))];
    if (valid.length) break;
  }
  const check = v => { const s = String(v ?? '').replace(/[,\s]/g, ''); return /^\d+$/.test(s) && valid.includes(Number(s)); };
  return {
    body: `<div class="prompt">יש לכתוב מספר ${pw}, ${dw} מ-<span class="ltr">${fmt(n)}</span>, המורכב מאותן ספרות.</div>`,
    parts: [{ type: 'text', check, placeholder: 'המספר:' }],
    hint: odd ? 'מספר אי-זוגי מסתיים בספרות 1, 3, 5, 7 או 9.' : 'מספר זוגי מסתיים בספרות 0, 2, 4, 6 או 8.',
    explain: q => {
      const mine = Number(String(q.parts[0].v ?? '').replace(/[,\s]/g, ''));
      const others = valid.filter(x => x !== mine);
      const list = others.slice(0, 3).map(fmt).join(', ');
      if (q.result) return others.length ? `אגב, אפשר היה גם: ${list}.` : 'זו הייתה האפשרות היחידה.';
      return `למשל: ${list}.`;
    }
  };
}

/* ---------- numbers in words ---------- */
const W_ONES = ['', 'אחת', 'שתיים', 'שלוש', 'ארבע', 'חמש', 'שש', 'שבע', 'שמונה', 'תשע'];
const W_TEENS = ['עשר', 'אחת עשרה', 'שתים עשרה', 'שלוש עשרה', 'ארבע עשרה', 'חמש עשרה', 'שש עשרה', 'שבע עשרה', 'שמונה עשרה', 'תשע עשרה'];
const W_TENS = ['', '', 'עשרים', 'שלושים', 'ארבעים', 'חמישים', 'שישים', 'שבעים', 'שמונים', 'תשעים'];
const W_THOU = ['', 'אלף', 'אלפיים', 'שלושת אלפים', 'ארבעת אלפים', 'חמשת אלפים', 'ששת אלפים', 'שבעת אלפים', 'שמונת אלפים', 'תשעת אלפים'];
function numWords(n) {
  const parts = [];
  const th = Math.floor(n / 1000), h = Math.floor(n % 1000 / 100), r = n % 100;
  if (th) parts.push(W_THOU[th]);
  if (h) parts.push(h === 1 ? 'מאה' : h === 2 ? 'מאתיים' : W_ONES[h] + ' מאות');
  if (r) {
    if (r < 10) parts.push(W_ONES[r]);
    else if (r < 20) parts.push(W_TEENS[r - 10]);
    else { parts.push(W_TENS[Math.floor(r / 10)]); if (r % 10) parts.push(W_ONES[r % 10]); }
  }
  if (parts.length > 1) parts[parts.length - 1] = 'ו' + parts[parts.length - 1];
  return parts.join(' ');
}
function genWords(t) {
  const n = t === 1 ? rnd(101, 999) : rnd(1001, 9999);
  const s = String(n);
  const decoys = new Set();
  let guard = 0;
  while (decoys.size < 3 && guard++ < 200) {
    let d;
    const k = rnd(0, 2);
    if (k === 0) { const a = s.split(''); const i = rnd(0, a.length - 2); [a[i], a[i + 1]] = [a[i + 1], a[i]]; d = Number(a.join('')); }
    else { const a = s.split(''); const i = rnd(0, a.length - 1); a[i] = String(rnd(0, 9)); d = Number(a.join('')); }
    if (d !== n && d > 99 && String(d).length === s.length) decoys.add(d);
  }
  if (Math.random() < .5) {
    return {
      body: `<div class="prompt">איזה מספר כתוב כאן במילים?</div><div class="prompt" style="font-size:26px">${numWords(n)}</div>`,
      parts: [{ type: 'buttons', opts: shuffle([n, ...decoys]).map(fmt), ans: fmt(n) }],
      hint: 'כדאי לכתוב את הספרות לפי המקום: אלפים, מאות, עשרות ויחידות.',
      explain: `${numWords(n)} = <span class="ltr">${fmt(n)}</span>`
    };
  }
  return {
    body: `<div class="prompt">יש לכתוב במספרים:</div><div class="prompt" style="font-size:26px">${numWords(n)}</div>`,
    parts: [{ type: 'num', ans: n }],
    hint: 'כדאי לכתוב את הספרות לפי המקום: אלפים, מאות, עשרות ויחידות.',
    explain: `${numWords(n)} = <span class="ltr">${fmt(n)}</span>`
  };
}

/* ---------- greater / smaller by N ---------- */
function genMoreLess(t) {
  const ds = t === 1 ? [10, 20, 50, 100, 200] : t === 2 ? [30, 59, 84, 100, 200, 400] : [59, 84, 100, 250, 400, 1000, 2000];
  const d = pick(ds);
  const R = t === 1 ? [200, 900] : [1000, 7000];
  if (Math.random() < .7) {
    const up = Math.random() < .5;
    const n = rnd(R[0] + (up ? 0 : d), R[1]);
    const ans = up ? n + d : n - d;
    return {
      body: `<div class="prompt">איזה מספר ${up ? 'גדול' : 'קטן'} ב-<span class="ltr">${fmt(d)}</span> מהמספר <span class="ltr">${fmt(n)}</span>?</div>`,
      parts: [{ type: 'num', ans }],
      hint: up ? 'גדול ב... פירושו להוסיף.' : 'קטן ב... פירושו לחסר.',
      explain: `<span class="ltr">${fmt(n)} ${up ? '+' : '−'} ${fmt(d)} = ${fmt(ans)}</span>`
    };
  }
  const b = rnd(R[0], R[1] - d), a = b + d;
  return {
    body: `<div class="prompt">בכמה המספר <span class="ltr">${fmt(a)}</span> גדול מהמספר <span class="ltr">${fmt(b)}</span>?</div>`,
    parts: [{ type: 'num', ans: d }],
    hint: 'כדי לדעת בכמה מספר אחד גדול מהשני, מחסרים את הקטן מהגדול.',
    explain: `<span class="ltr">${fmt(a)} − ${fmt(b)} = ${fmt(d)}</span>`
  };
}

/* ---------- compare place-value expressions ---------- */
function genPlaceCmp(t) {
  const mk = () => {
    const kind = pick(['h', 'ht', 'tu', 'th']);
    if (kind === 'h') { const h = rnd(1, 9); return { txt: `${h} מאות`, v: h * 100 }; }
    if (kind === 'ht') { const h = rnd(1, 9), tn = rnd(1, 9); return { txt: `${h} מאות ו-${tn} עשרות`, v: h * 100 + tn * 10 }; }
    if (kind === 'tu') { const tn = rnd(5, 60), u = rnd(1, 25); return { txt: `${tn} עשרות ו-${u} יחידות`, v: tn * 10 + u }; }
    const th = rnd(1, 9); return { txt: `${th} אלפים`, v: th * 1000 };
  };
  let A = mk(), B = mk();
  if (t === 1) { while (A.v >= 1000 || B.v >= 1000) { A = mk(); B = mk(); } }
  if (Math.random() < .25 && A.v % 10 === 0) B = { txt: `${A.v / 10} עשרות`, v: A.v };
  const sym = A.v < B.v ? '<' : A.v > B.v ? '>' : '=';
  const box = x => `<span dir="rtl" style="unicode-bidi:isolate;background:#fff8;border-radius:12px;padding:4px 8px;font-weight:800;flex:1 1 0;text-align:center;min-width:0">${x}</span>`;
  return {
    body: `<div class="prompt">יש לסמן את הסימן המתאים:</div><div class="prompt" style="direction:ltr;display:flex;gap:10px;justify-content:center;align-items:center;flex-wrap:nowrap;font-size:clamp(15px,4.4vw,22px)">${box(A.txt)}<b>?</b>${box(B.txt)}</div>`,
    parts: [{ type: 'buttons', opts: ['>', '=', '<'], ans: sym }],
    hint: 'כדאי להפוך כל צד למספר רגיל: מאה היא 100, עשר היא 10, אלף הוא 1,000.',
    explain: `${A.txt} = ${fmt(A.v)} ו-${B.txt} = ${fmt(B.v)}. <span class="ltr">${fmt(A.v)} ${sym === '<' ? '&lt;' : sym === '>' ? '&gt;' : '='} ${fmt(B.v)}</span>`
  };
}

/* ---------- missing number with helper exercise ---------- */
function genEquation(t) {
  const R = t === 1 ? [20, 99] : t === 2 ? [100, 600] : [300, 4000];
  const kind = pick(['add', 'sub1', 'sub2']);
  let a = rnd(R[0], R[1]), b = rnd(R[0], R[1]);
  while (b === a) b = rnd(R[0], R[1]);
  let eq, helper, wrong, ans;
  if (kind === 'add') { const c = a + b; eq = `${fmt(a)} + ___ = ${fmt(c)}`; helper = `${fmt(c)} − ${fmt(a)}`; wrong = [`${fmt(c)} + ${fmt(a)}`, `${fmt(a)} − ${fmt(c)}`]; ans = b; }
  else if (kind === 'sub1') { const A = a + b; eq = `${fmt(A)} − ___ = ${fmt(a)}`; helper = `${fmt(A)} − ${fmt(a)}`; wrong = [`${fmt(A)} + ${fmt(a)}`, `${fmt(a)} − ${fmt(A)}`]; ans = b; }
  else { const A = a + b; eq = `___ − ${fmt(a)} = ${fmt(b)}`; helper = `${fmt(a)} + ${fmt(b)}`; wrong = [`${fmt(b)} − ${fmt(a)}`, `${fmt(a)} − ${fmt(b)}`]; ans = A; }
  const eqText = eq.replace('___', '___');
  return {
    body: `<div class="prompt">יש להשלים את המספר החסר:<br><span class="ltr" style="font-size:30px;margin-top:8px">${eqText}</span></div>`,
    parts: [
      { type: 'buttons', label: 'תרגיל עזר', ltr: true, opts: shuffle([helper, ...wrong]), ans: helper },
      { type: 'num', label: 'המספר החסר', ans }
    ],
    hint: 'כדי למצוא מספר חסר בוחרים תרגיל עזר הפוך: חיסור בודק חיבור, וחיבור בודק חיסור.',
    explain: `תרגיל העזר: <span class="ltr">${helper} = ${fmt(ans)}</span>. כך מתקבל המספר החסר ${fmt(ans)}.`
  };
}

/* ---------- multiplication ---------- */
function genMult(t) {
  const facts = t === 1 ? [2, 5, 10] : t === 2 ? [3, 4, 6] : [6, 7, 8, 9];
  const a = pick(facts), b = rnd(2, 10);
  const [x, y] = Math.random() < .5 ? [a, b] : [b, a];
  const p = x * y;
  if (Math.random() < .25) {
    return {
      body: `<div class="prompt"><span class="ltr" style="font-size:34px">___ × ${x} = ${p}</span></div>`,
      parts: [{ type: 'num', ans: y }],
      hint: `כמה פעמים צריך לקחת ${x} כדי לקבל ${p}?`,
      explain: `<span class="ltr">${y} × ${x} = ${p}</span>`
    };
  }
  return {
    body: `<div class="prompt"><span class="ltr" style="font-size:34px">${x} × ${y} = ?</span></div>`,
    parts: [{ type: 'num', ans: p }],
    hint: `אפשר לחבר ${y} פעמים את המספר ${x}, או להיעזר בלוח הכפל.`,
    explain: `<span class="ltr">${x} × ${y} = ${p}</span>`
  };
}

/* ---------- word problems ---------- */
function genWord(t) {
  const R = t === 1 ? [20, 90] : t === 2 ? [120, 600] : [300, 3000];
  const names = [['גל', 1], ['נועם', 0], ['אדיר', 0], ['שירה', 1], ['דניאל', 0], ['מאיה', 1]];
  const [nm, fem] = pick(names);
  const [nm2, fem2] = pick(names.filter(x => x[0] !== nm));
  const a = rnd(R[0], R[1]), b = rnd(R[0] / 2 | 0, Math.min(R[1], a - 1));
  const g = rnd(2, t === 1 ? 5 : 9), k = rnd(2, t === 1 ? 6 : 9);
  const T = [
    () => ({ q: `בספרייה יש ${fmt(a)} ספרים. השאילו ${fmt(b)} ספרים. כמה ספרים נשארו בספרייה?`, ex: `${fmt(a)} − ${fmt(b)}`, ans: a - b, h: 'השאילו אומר שהספרים יצאו, ולכן מחסרים.' }),
    () => ({ q: `בחנות היו ${fmt(a)} תפוחים. הגיעו עוד ${fmt(b)} תפוחים. כמה תפוחים יש עכשיו בחנות?`, ex: `${fmt(a)} + ${fmt(b)}`, ans: a + b, h: 'הגיעו עוד אומר שהכמות גדלה, ולכן מחברים.' }),
    () => ({ q: `בכל שקית יש ${g} סוכריות. יש ${k} שקיות. כמה סוכריות יש בכל השקיות?`, ex: `${g} × ${k}`, ans: g * k, h: 'כמות זהה בכל קבוצה: מכפילים את מספר הקבוצות בגודל קבוצה.' }),
    () => ({ q: `בכיתה א' יש ${fmt(a)} ילדים ובכיתה ב' יש ${fmt(b)} ילדים. בכמה ילדים יש יותר בכיתה א'?`, ex: `${fmt(a)} − ${fmt(b)}`, ans: a - b, h: 'כשרוצים לדעת בכמה יש יותר, מחסרים את הקטן מהגדול.' }),
    () => ({ q: `ל${nm} יש ${fmt(a)} מדבקות. ל${nm2} יש ${fmt(b)} מדבקות פחות מל${nm}. כמה מדבקות יש ל${nm2}?`, ex: `${fmt(a)} − ${fmt(b)}`, ans: a - b, h: 'פחות מ... פירושו להחסיר.' }),
    () => { const c = rnd(R[0] / 2 | 0, R[1]); return { q: `באוטובוס היו ${fmt(a)} נוסעים. ירדו ${fmt(b)} נוסעים ועלו ${fmt(c)} נוסעים. כמה נוסעים יש באוטובוס עכשיו?`, ex: `${fmt(a)} − ${fmt(b)} + ${fmt(c)}`, ans: a - b + c, h: 'קודם מחסרים את מי שירד, ואחר כך מוסיפים את מי שעלה.' }; }
  ];
  const w = pick(T.slice(0, t === 1 ? 5 : 6))();
  return {
    body: `<div class="prompt" style="font-size:22px">${w.q}</div>`,
    parts: [{ type: 'num', ans: w.ans }],
    hint: w.h,
    explain: `התרגיל: <span class="ltr">${w.ex} = ${fmt(w.ans)}</span>`
  };
}

/* ---------- number line with an arrow ---------- */
function numLineWrite(t) {
  const step = t === 1 ? 10 : pick([10, 100]);
  const span = step * 10;
  const start = step === 10 ? rnd(1, t === 1 ? 9 : 90) * 100 : rnd(1, 8) * 1000;
  const idx = rnd(1, 9), val = start + idx * step;
  const x0 = 30, x1 = 290, y = 80;
  let ticks = '';
  for (let i = 0; i <= 10; i++) {
    const x = x0 + (x1 - x0) * i / 10;
    ticks += `<line x1="${x}" y1="${y - (i % 5 ? 8 : 14)}" x2="${x}" y2="${y + (i % 5 ? 8 : 14)}" stroke="#163b2a" stroke-width="${i % 5 ? 2 : 3}"/>`;
  }
  const ax = x0 + (x1 - x0) * idx / 10;
  const svg = `<svg class="numline" viewBox="0 0 320 150" style="display:block;margin:6px auto" role="img" aria-label="ישר מספרים"><line x1="${x0 - 10}" y1="${y}" x2="${x1 + 10}" y2="${y}" stroke="#163b2a" stroke-width="4"/>${ticks}<text x="${x0}" y="${y + 38}" text-anchor="middle" font-size="17" font-weight="800" fill="#163b2a" direction="ltr">${fmt(start)}</text><text x="${x1}" y="${y + 38}" text-anchor="middle" font-size="17" font-weight="800" fill="#163b2a">${fmt(start + span)}</text><text x="${(x0 + x1) / 2}" y="${y + 38}" text-anchor="middle" font-size="17" font-weight="800" fill="#163b2a">${fmt(start + span / 2)}</text><path d="M${ax} ${y - 16} l-9 -22 h6 v-18 h6 v18 h6 z" fill="#d84a2b" stroke="#7a1f0e" stroke-width="2"/></svg>`;
  return {
    body: `<div class="prompt">איזה מספר מסומן בחץ?</div>${svg}`,
    parts: [{ type: 'num', ans: val }],
    hint: `בין שני המספרים הכתובים יש 10 קפיצות שוות. כל קפיצה היא ${fmt(step)}.`,
    explain: `כל קפיצה היא ${fmt(step)}. החץ נמצא אחרי ${idx} קפיצות מ-${fmt(start)}, ולכן המספר הוא ${fmt(val)}.`
  };
}

/* ---------- vertical arithmetic ---------- */
function vertHTML(a, b, op) {
  const sa = String(a), sb = String(b), n = Math.max(sa.length, sb.length);
  const cells = s => [...s.padStart(n, ' ')].map(c => `<td>${c.trim()}</td>`).join('');
  return `<table class="vert" dir="ltr"><tr><td class="vs"></td>${cells(sa)}</tr><tr><td class="vs">${op}</td>${cells(sb)}</tr><tr class="vl"><td class="vs"></td><td colspan="${n}"></td></tr><tr><td class="vs"></td><td colspan="${n}" class="vq">?</td></tr></table>`;
}
function hasCarry(a, b, op) {
  let x = a, y = b, c = 0;
  while (x > 0 || y > 0) {
    const dx = x % 10, dy = y % 10;
    if (op === '+') { if (dx + dy + c > 9) return true; c = 0; } else { if (dx - c < dy) return true; c = 0; }
    x = Math.floor(x / 10); y = Math.floor(y / 10);
  }
  return false;
}
function genColumn(t) {
  const [lo, hi] = t === 1 ? [10, 99] : t === 2 ? [100, 999] : [1000, 9999];
  const op = pick(['+', '−']);
  let a, b;
  for (let i = 0; i < 40; i++) {
    a = rnd(lo, hi); b = rnd(lo, hi);
    if (op === '+') { if (a + b > 9999) continue; } else if (a < b) [a, b] = [b, a];
    if (hasCarry(a, b, op) || i > 30) break;
  }
  const ans = op === '+' ? a + b : a - b;
  const vertical = Math.random() < .7;
  const body = vertical
    ? `<div class="prompt">יש לפתור במאונך:</div>${vertHTML(a, b, op)}`
    : `<div class="prompt" style="font-size:36px"><span class="ltr">${fmt(a)} ${op} ${fmt(b)} = ?</span></div>`;
  return {
    body, sig: String(a) + op + b,
    parts: [{ type: 'num', ans }],
    hint: op === '+' ? 'מתחילים מהיחידות. אם הסכום גדול מ-9, כותבים את היחידות ומעבירים את העשרת לטור הבא.' : 'מתחילים מהיחידות. אם אי אפשר לחסר, לוקחים עשרה מהטור השמאלי.',
    explain: `<span class="ltr">${fmt(a)} ${op} ${fmt(b)} = ${fmt(ans)}</span>`
  };
}

let angBag = [], angDrawBag = [];
function bagPick(bag, items) { if (!bag.length) bag.push(...shuffle(items.slice())); return bag.pop(); }
function genAngleId() {
  const cls = bagPick(angBag, ['חדה', 'ישרה', 'קהה', 'שטוחה']);
  const deg = cls === 'חדה' ? pick([20, 30, 40, 55, 65, 75, 82]) : cls === 'ישרה' ? 90 : cls === 'שטוחה' ? 180 : pick([100, 110, 120, 135, 150, 165]);
  const cx = 160, cy = 170, L = 110;
  const rad = deg * Math.PI / 180;
  const x2 = (cx + L * Math.cos(rad)).toFixed(1), y2 = (cy - L * Math.sin(rad)).toFixed(1);
  const svg = `<svg class="angle" viewBox="0 0 320 220" role="img" aria-label="זווית"><line x1="${cx}" y1="${cy}" x2="${cx + L}" y2="${cy}" stroke="#163b2a" stroke-width="8" stroke-linecap="round"/><line x1="${cx}" y1="${cy}" x2="${x2}" y2="${y2}" stroke="#163b2a" stroke-width="8" stroke-linecap="round"/><circle cx="${cx}" cy="${cy}" r="8" fill="#f0a430"/></svg>`;
  return {
    body: `${svg}<div class="prompt">איזה סוג זווית מוצג?</div>`,
    parts: [{ type: 'buttons', opts: ['חדה', 'ישרה', 'קהה', 'שטוחה'], ans: angleClass(deg) }],
    hint: 'זווית ישרה נראית כמו פינה של מרובע. חדה קטנה ממנה, קהה גדולה ממנה.',
    explain: `הזווית היא ${angleClass(deg)}.`
  };
}

function genAngleDraw() {
  const target = bagPick(angDrawBag, ['חדה', 'ישרה', 'קהה']);
  const text = { 'חדה': 'יש לשרטט זווית חדה', 'ישרה': 'יש לשרטט זווית ישרה', 'קהה': 'יש לשרטט זווית קהה' }[target];
  const check = v => {
    if (typeof v !== 'number') return false;
    if (target === 'חדה') return v > 0 && v < 90;
    if (target === 'ישרה') return v === 90;
    return v > 90 && v < 180;
  };
  return {
    body: `<div class="prompt compact">${text}</div>`,
    drawInit: target === 'ישרה' ? pick([30, 45, 135, 150]) : 90,
    parts: [{ type: 'draw', check, help: { 'חדה': 'מקרבים את הקו הירוק אל הקו השחור, עד שהזווית קטנה יותר מפינה של מרובע.', 'ישרה': 'מעמידים את הקו הירוק בניצב לקו השחור, כך שייווצרו פינה של מרובע.', 'קהה': 'מרחיקים את הקו הירוק מהקו השחור, עד שהזווית גדולה מפינה של מרובע אבל עדיין לא קו ישר.' }[target] }],
    hint: 'יש לגרור את הקצה הצהוב למיקום המתאים.',
    explain: target === 'ישרה' ? 'שורטטה זווית ישרה. הריבוע הקטן בפינה מסמן זווית ישרה.' : `שורטטה זווית ${target}.`
  };
}

const CATS = [
  { id: 'digit', name: 'שינוי ספרה', animal: '🦁', gen: genDigit },
  { id: 'compare', name: 'סימני <&nbsp;>&nbsp;=', animal: '🦉', gen: t => Math.random() < .35 ? genPlaceCmp(t) : genCompare(t) },
  { id: 'nocalc', name: 'השוואה בלי חישוב', animal: '🐯', gen: genNoCalc },
  { id: 'decomp', name: 'פירוק מספר', animal: '🐨', gen: genDecomp },
  { id: 'order', name: 'סידור מספרים', animal: '🦓', gen: genOrder },
  { id: 'numline', name: 'ישר המספרים', animal: '🦧', gen: t => Math.random() < .6 ? numLineWrite(t) : genNumLine(t) },
  { id: 'seq', name: 'סדרות', animal: '🐸', gen: t => Math.random() < .4 ? genSeqMember(t) : genSeq(t) },
  { id: 'samedigits', name: 'אותן ספרות', animal: '🦥', gen: genSameDigits },
  { id: 'column', name: 'חיבור וחיסור', animal: '🐒', gen: genColumn },
  { id: 'angleid', name: 'סוגי זוויות', animal: '🦅', gen: genAngleId },
  { id: 'angledraw', name: 'שרטוט זווית', animal: '🐍', gen: genAngleDraw },
  { id: 'words', name: 'מספר במילים', animal: '🦒', gen: genWords },
  { id: 'moreless', name: 'גדול וקטן ב...', animal: '🐘', gen: genMoreLess },
  { id: 'equation', name: 'מספר חסר', animal: '🦔', gen: genEquation },
  { id: 'mult', name: 'לוח הכפל', animal: '🦏', gen: genMult },
  { id: 'word', name: 'בעיות מילוליות', animal: '🐊', gen: genWord }
];

/* ---------- state ---------- */
/* ---------- the teacher's review sheets: exact exercises, served before generated ones ---------- */
const symOf = (a, b) => a < b ? '<' : a > b ? '>' : '=';
const symH = s => s === '<' ? '&lt;' : s === '>' ? '&gt;' : '=';
const cmpBox = x => `<span dir="rtl" style="unicode-bidi:isolate;background:#fff8;border-radius:12px;padding:4px 8px;font-weight:800;flex:1 1 0;text-align:center;min-width:0">${x}</span>`;
function qPlace(A, Av, B, Bv) {
  const s = symOf(Av, Bv);
  return {
    body: `<div class="prompt">יש לסמן את הסימן המתאים:</div><div class="prompt" style="direction:ltr;display:flex;gap:10px;justify-content:center;align-items:center;flex-wrap:nowrap;font-size:clamp(15px,4.4vw,22px)">${cmpBox(A)}<b>?</b>${cmpBox(B)}</div>`,
    parts: [{ type: 'buttons', opts: ['>', '=', '<'], ans: s }],
    hint: 'כדאי להפוך כל צד למספר רגיל: מאה היא 100, עשר היא 10, אלף הוא 1,000.',
    explain: `${A} = ${fmt(Av)} ו-${B} = ${fmt(Bv)}. <span class="ltr">${fmt(Av)} ${symH(s)} ${fmt(Bv)}</span>`
  };
}
function qDigit(n, i, e, how) {
  const s = String(n), len = s.length, old = Number(s[i]), pv = 10 ** (len - 1 - i);
  const diff = (e - old) * pv, amount = Math.abs(diff), grows = diff > 0;
  const what = how === 'place' ? `את ספרת ${PLACE[pv]}` : `את הספרה ${old}`;
  return {
    body: `<div class="prompt">במספר <span class="ltr">${fmt(n)}</span> שינו ${what} ל-${e}.<br>האם המספר החדש גדל או קטן, ובכמה?</div>`,
    parts: [{ type: 'buttons', opts: ['גדל', 'קטן'], ans: grows ? 'גדל' : 'קטן' }, { type: 'num', label: 'בכמה', ans: amount }],
    hint: 'כדאי לשים לב לאיזה מקום שייכת הספרה. ההפרש מוכפל בערך המקום.',
    explain: `הספרה ${old} נמצאת במקום ${PLACE[pv]}. <span class="ltr">${fmt(n)}</span> הופך ל-<span class="ltr">${fmt(n + diff)}</span>, לכן המספר ${grows ? 'גדל' : 'קטן'} ב-${fmt(amount)}.`
  };
}
function qDecomp(n, shown, ans) {
  return {
    body: `<div class="prompt">יש להשלים את הפירוק:<br><span class="ltr">${fmt(n)} = ${shown}</span></div>`,
    parts: [{ type: 'num', ans }],
    hint: 'כל ספרה שווה לערך שלה לפי המקום.',
    explain: `החסר הוא ${fmt(ans)}. <span class="ltr">${fmt(n)} = ${shown.replace('___', fmt(ans))}</span>`
  };
}
function qWordsPick(n, decoys) {
  return {
    body: `<div class="prompt">איך כותבים במילים את המספר <span class="ltr">${fmt(n)}</span>?</div>`,
    parts: [{ type: 'buttons', list: true, opts: shuffle([n, ...decoys]).map(numWords), ans: numWords(n) }],
    hint: 'כדאי לקרוא לפי המקום: אלפים, מאות, עשרות ויחידות.',
    explain: `<span class="ltr">${fmt(n)}</span> = ${numWords(n)}`
  };
}
function qMoreLess(n, d, up) {
  const ans = up ? n + d : n - d;
  return {
    body: `<div class="prompt">איזה מספר ${up ? 'גדול' : 'קטן'} ב-<span class="ltr">${fmt(d)}</span> מהמספר <span class="ltr">${fmt(n)}</span>?</div>`,
    parts: [{ type: 'num', ans }],
    hint: up ? 'גדול ב... פירושו להוסיף.' : 'קטן ב... פירושו לחסר.',
    explain: `<span class="ltr">${fmt(n)} ${up ? '+' : '−'} ${fmt(d)} = ${fmt(ans)}</span>`
  };
}
function qSame(n, odd, smaller) {
  const d = String(n).split('');
  const valid = [...new Set(perms(d).filter(x => x[0] !== '0').map(x => Number(x.join(''))).filter(v => (smaller ? v < n : v > n) && (v % 2 === 1) === odd))];
  const check = v => { const s = String(v ?? '').replace(/[,\s]/g, ''); return /^\d+$/.test(s) && valid.includes(Number(s)); };
  return {
    body: `<div class="prompt">יש לכתוב מספר ${odd ? 'אי-זוגי' : 'זוגי'}, ${smaller ? 'הקטן' : 'הגדול'} מ-<span class="ltr">${fmt(n)}</span>, המורכב מאותן ספרות.</div>`,
    parts: [{ type: 'text', check, placeholder: 'המספר:' }],
    hint: odd ? 'מספר אי-זוגי מסתיים בספרות 1, 3, 5, 7 או 9.' : 'מספר זוגי מסתיים בספרות 0, 2, 4, 6 או 8.',
    explain: q => {
      const mine = Number(String(q.parts[0].v ?? '').replace(/[,\s]/g, ''));
      const others = valid.filter(x => x !== mine).slice(0, 3).map(fmt).join(', ');
      return q.result ? (others ? `אגב, אפשר היה גם: ${others}.` : 'זו הייתה האפשרות היחידה.') : `למשל: ${others}.`;
    }
  };
}
function qOrder(nums) {
  const sorted = [...nums].sort((x, y) => x - y);
  return {
    body: `<div class="prompt">יש ללחוץ או לגרור את המספרים מהקטן לגדול.</div>`,
    parts: [{ type: 'order', items: [...nums], ans: sorted }],
    hint: 'מומלץ להשוות קודם את מספר הספרות, ואז את הספרות השמאליות ביותר.',
    explain: `הסדר הנכון: <span class="ltr">${sorted.map(fmt).join(' &lt; ')}</span>`
  };
}
function qSeq(terms, blanks) {
  const k = Math.abs(terms[1] - terms[0]);
  const shown = terms.map((v, i) => blanks.includes(i) ? `<span class="gap">חסר ${blanks.indexOf(i) + 1}</span>` : fmt(v)).join(', ');
  return {
    body: `<div class="prompt">יש להשלים את הסדרה. היא ממשיכה באותן הקפיצות:<br><span class="ltr" style="font-size:28px;margin-top:10px">${shown}</span></div>`,
    parts: blanks.map((bi, j) => ({ type: 'num', label: `חסר ${j + 1}`, ans: terms[bi] })),
    hint: 'כדאי לבדוק בכמה גדל או קטן כל מספר לעומת המספר שלפניו.',
    explain: `בכל שלב יש קפיצה של ${fmt(k)}. הסדרה המלאה: ${terms.map(fmt).join(', ')}`
  };
}
function qSeqMember(start, k, X) {
  const isIn = (X - start) % k === 0 && X >= start;
  const shown = [0, 1, 2, 3].map(i => fmt(start + i * k)).join(', ');
  return {
    body: `<div class="prompt">סדרה: <span class="ltr">${shown}, ...</span><br>האם המספר <span class="ltr" style="font-size:32px">${fmt(X)}</span> יופיע בהמשך הסדרה?</div>`,
    parts: [{ type: 'buttons', opts: ['כן', 'לא'], ans: isIn ? 'כן' : 'לא' }],
    hint: 'יש לבדוק אם ההפרש בין המספר המבוקש למספר הראשון מתחלק בקפיצה.',
    explain: `המספר ${isIn ? 'אכן יופיע' : 'לא יופיע'}: הקפיצה היא ${fmt(k)}, וכל המספרים בסדרה מסתיימים ב-${String(start).slice(-1)}.`
  };
}
function segSvg(a, b) {
  return `<svg class="numline" viewBox="0 0 320 110" style="display:block;margin:4px auto" role="img" aria-label="ישר מספרים"><line x1="10" y1="45" x2="300" y2="45" stroke="#163b2a" stroke-width="3"/><path d="M300 45 l-12 -7 v14 z" fill="#163b2a"/><line x1="70" y1="45" x2="200" y2="45" stroke="#163b2a" stroke-width="12"/><line x1="70" y1="30" x2="70" y2="60" stroke="#163b2a" stroke-width="3"/><line x1="200" y1="30" x2="200" y2="60" stroke="#163b2a" stroke-width="3"/><text x="70" y="88" text-anchor="middle" font-size="18" font-weight="800" fill="#163b2a">${fmt(a)}</text><text x="200" y="88" text-anchor="middle" font-size="18" font-weight="800" fill="#163b2a">${fmt(b)}</text></svg>`;
}
function qSegPick(a, b, opts) {
  const inside = opts.find(x => x > a && x < b);
  return {
    body: `<div class="prompt">איזה מספר נמצא בקטע המודגש בישר המספרים?</div>${segSvg(a, b)}`,
    parts: [{ type: 'buttons', opts: opts.map(fmt), ans: fmt(inside) }],
    hint: 'המספר צריך להיות גדול מהמספר הקטן וקטן מהמספר הגדול.',
    explain: `<span class="ltr">${fmt(inside)}</span> נמצא בין <span class="ltr">${fmt(a)}</span> ל-<span class="ltr">${fmt(b)}</span>.`
  };
}
function qSegWrite(a, b) {
  const check = v => { const n = parseNum(v); return n > a && n < b; };
  return {
    body: `<div class="prompt">יש לכתוב מספר נוסף שנמצא בקטע המודגש בישר המספרים.</div>${segSvg(a, b)}`,
    parts: [{ type: 'text', check, placeholder: 'המספר:' }],
    hint: 'המספר צריך להיות גדול מהמספר הקטן וקטן מהמספר הגדול.',
    explain: `כל מספר בין <span class="ltr">${fmt(a)}</span> ל-<span class="ltr">${fmt(b)}</span> מתאים, למשל <span class="ltr">${fmt(a + 25)}</span>.`
  };
}
function qCol(a, op, b) {
  const ans = op === '+' ? a + b : a - b;
  return {
    body: `<div class="prompt">יש לפתור במאונך:</div>${vertHTML(a, b, op)}`, sig: String(a) + op + b,
    parts: [{ type: 'num', ans }],
    hint: op === '+' ? 'מתחילים מהיחידות. אם הסכום גדול מ-9, כותבים את היחידות ומעבירים את העשרת לטור הבא.' : 'מתחילים מהיחידות. אם אי אפשר לחסר, לוקחים עשרה מהטור השמאלי.',
    explain: `<span class="ltr">${fmt(a)} ${op} ${fmt(b)} = ${fmt(ans)}</span>`
  };
}
function qEq(kind, a, b) {
  let eq, helper, wrong, ans;
  if (kind === 'add') { eq = `${fmt(a)} + ___ = ${fmt(b)}`; helper = `${fmt(b)} − ${fmt(a)}`; wrong = [`${fmt(b)} + ${fmt(a)}`, `${fmt(a)} − ${fmt(b)}`]; ans = b - a; }
  else if (kind === 'sub1') { eq = `${fmt(a)} − ___ = ${fmt(b)}`; helper = `${fmt(a)} − ${fmt(b)}`; wrong = [`${fmt(a)} + ${fmt(b)}`, `${fmt(b)} − ${fmt(a)}`]; ans = a - b; }
  else { eq = `___ − ${fmt(a)} = ${fmt(b)}`; helper = `${fmt(a)} + ${fmt(b)}`; wrong = [`${fmt(b)} − ${fmt(a)}`, `${fmt(a)} − ${fmt(b)}`]; ans = a + b; }
  return {
    body: `<div class="prompt">יש להשלים את המספר החסר:<br><span class="ltr" style="font-size:30px;margin-top:8px">${eq}</span></div>`,
    parts: [{ type: 'buttons', label: 'תרגיל עזר', ltr: true, opts: shuffle([helper, ...wrong]), ans: helper }, { type: 'num', label: 'המספר החסר', ans }],
    hint: 'כדי למצוא מספר חסר בוחרים תרגיל עזר הפוך: חיסור בודק חיבור, וחיבור בודק חיסור.',
    explain: `תרגיל העזר: <span class="ltr">${helper} = ${fmt(ans)}</span>. כך מתקבל המספר החסר ${fmt(ans)}.`
  };
}
function qMult(x, y) {
  return {
    body: `<div class="prompt"><span class="ltr" style="font-size:34px">${x} × ${y} = ?</span></div>`,
    parts: [{ type: 'num', ans: x * y }],
    hint: `אפשר לחבר ${y} פעמים את המספר ${x}, או להיעזר בלוח הכפל.`,
    explain: `<span class="ltr">${x} × ${y} = ${x * y}</span>`
  };
}
function qNoCalc(L, lv, R, rv, hint) {
  const s = symOf(lv, rv);
  return {
    body: `<div class="prompt">יש לסמן בלי לפתור את התרגילים:</div><div class="prompt" style="font-size:28px"><span class="ltr">${L} &nbsp; ? &nbsp; ${R}</span></div>`,
    parts: [{ type: 'buttons', opts: ['>', '=', '<'], ans: s }],
    hint,
    explain: `הסימן המתאים הוא <span class="ltr">${symH(s)}</span>.`
  };
}
function qWordP(q, ex, ans, h) {
  return { body: `<div class="prompt" style="font-size:22px">${q}</div>`, parts: [{ type: 'num', ans }], hint: h, explain: `התרגיל: <span class="ltr">${ex} = ${fmt(ans)}</span>` };
}
function qAngle(deg, rot) {
  const cx = 160, cy = 120, L = 100;
  const pt = d => { const r = d * Math.PI / 180; return [(cx + L * Math.cos(r)).toFixed(1), (cy - L * Math.sin(r)).toFixed(1)]; };
  const [x1, y1] = pt(rot), [x2, y2] = pt(rot + deg);
  const svg = `<svg class="angle" viewBox="0 0 320 240" role="img" aria-label="זווית"><line x1="${cx}" y1="${cy}" x2="${x1}" y2="${y1}" stroke="#163b2a" stroke-width="8" stroke-linecap="round"/><line x1="${cx}" y1="${cy}" x2="${x2}" y2="${y2}" stroke="#163b2a" stroke-width="8" stroke-linecap="round"/><circle cx="${cx}" cy="${cy}" r="8" fill="#f0a430"/></svg>`;
  return {
    body: `${svg}<div class="prompt">איזה סוג זווית מוצג?</div>`,
    parts: [{ type: 'buttons', opts: ['חדה', 'ישרה', 'קהה', 'שטוחה'], ans: angleClass(deg) }],
    hint: 'זווית ישרה נראית כמו פינה של מרובע. חדה קטנה ממנה, קהה גדולה ממנה.',
    explain: `הזווית היא ${angleClass(deg)}.`
  };
}
function qAnglePics() {
  return {
    body: `<div class="prompt">באיזה ציור מסומנת זווית קהה?</div>`,
    parts: [{ type: 'buttons', opts: ['📏 פינת סרגל', '✏️ חוד עיפרון', '💻 מחשב נייד פתוח', '✂️ מספריים פתוחים'], ans: '💻 מחשב נייד פתוח' }],
    hint: 'זווית קהה גדולה מפינה של מרובע, אבל עדיין לא קו ישר.',
    explain: 'מסך של מחשב נייד פתוח לאחור יוצר זווית קהה. פינת הסרגל היא זווית ישרה, וחוד העיפרון והמספריים יוצרים זוויות חדות.'
  };
}
const SHEET = [
  ['compare', () => qPlace('4 מאות', 400, '30 עשרות ו-22 יחידות', 322)],
  ['compare', () => qPlace('5 אלפים', 5000, '4 אלפים, 3 מאות ו-24 עשרות', 4540)],
  ['compare', () => qPlace('4 מאות ו-15 עשרות', 550, '5 מאות', 500)],
  ['compare', () => qPlace('18 עשרות', 180, '16 עשרות ו-32 יחידות', 192)],
  ['compare', () => qPlace('60 עשרות ו-32 יחידות', 632, '7 מאות', 700)],
  ['digit', () => qDigit(4673, 0, 2)],
  ['digit', () => qDigit(5209, 1, 7)],
  ['digit', () => qDigit(3098, 1, 4, 'place')],
  ['digit', () => qDigit(2938, 2, 5, 'place')],
  ['digit', () => qDigit(4532, 1, 9)],
  ['digit', () => qDigit(3607, 1, 2, 'place')],
  ['decomp', () => qDecomp(124, '100 + ___ + 4', 20)],
  ['decomp', () => qDecomp(3145, '3,000 + ___ + 40 + 5', 100)],
  ['decomp', () => qDecomp(2046, '2,000 + ___ + 6', 40)],
  ['decomp', () => qDecomp(2459, '2,000 + ___ + 50 + 9', 400)],
  ['words', () => qWordsPick(5784, [5874, 5748, 4785])],
  ['moreless', () => qMoreLess(5784, 200, true)],
  ['moreless', () => qMoreLess(5784, 84, false)],
  ['samedigits', () => qSame(5784, true, true)],
  ['words', () => qWordsPick(2769, [2796, 2679, 7269])],
  ['moreless', () => qMoreLess(2769, 100, true)],
  ['moreless', () => qMoreLess(2769, 59, false)],
  ['samedigits', () => qSame(2769, false, false)],
  ['order', () => qOrder([2142, 899, 3099, 4001, 2098, 3198])],
  ['order', () => qOrder([3452, 1409, 3099, 2456, 2098, 999, 1097])],
  ['seq', () => qSeq([452, 462, 472, 482, 492, 502, 512], [2, 3, 6])],
  ['seq', () => qSeqMember(452, 10, 515)],
  ['seq', () => qSeqMember(452, 10, 532)],
  ['seq', () => qSeq([6500, 5500, 4500, 3500, 2500, 1500], [3, 4])],
  ['seq', () => qSeq([2983, 2984, 2985, 2986, 2987], [0, 3, 4])],
  ['seq', () => qSeq([134, 154, 174, 194, 214], [2, 3])],
  ['seq', () => qSeq([133, 136, 139, 142, 145], [2, 3])],
  ['numline', () => qSegPick(3670, 3770, [3780, 3681, 3657, 3791])],
  ['numline', () => qSegWrite(3670, 3770)],
  ['column', () => qCol(437, '+', 278)],
  ['column', () => qCol(387, '+', 179)],
  ['column', () => qCol(408, '+', 187)],
  ['column', () => qCol(548, '+', 342)],
  ['column', () => qCol(653, '+', 249)],
  ['column', () => qCol(239, '+', 458)],
  ['column', () => qCol(500, '−', 175)],
  ['column', () => qCol(472, '−', 56)],
  ['column', () => qCol(436, '−', 147)],
  ['column', () => qCol(568, '−', 349)],
  ['column', () => qCol(600, '−', 347)],
  ['column', () => qCol(741, '−', 239)],
  ['column', () => qCol(239, '+', 175)],
  ['equation', () => qEq('add', 348, 742)],
  ['equation', () => qEq('sub1', 405, 237)],
  ['equation', () => qEq('sub2', 204, 205)],
  ['equation', () => qEq('add', 546, 871)],
  ['equation', () => qEq('sub1', 763, 249)],
  ['equation', () => qEq('sub2', 193, 273)],
  ['equation', () => qEq('sub1', 432, 237)],
  ['equation', () => qEq('add', 537, 642)],
  ['equation', () => qEq('sub2', 146, 579)],
  ['mult', () => qMult(5, 5)],
  ['mult', () => qMult(7, 3)],
  ['mult', () => qMult(6, 4)],
  ['mult', () => qMult(8, 4)],
  ['mult', () => qMult(5, 6)],
  ['mult', () => qMult(5, 4)],
  ['mult', () => qMult(8, 3)],
  ['nocalc', () => qNoCalc('6,000 − 1,879', 4121, '7,000 − 1,879', 5121, 'מחסירים אותו מספר. ככל שהמספר הראשון גדול יותר, התוצאה גדולה יותר.')],
  ['nocalc', () => qNoCalc('3,042 − 1,879', 1163, '3,042 − 2,049', 993, 'המספר הראשון זהה. כשמחסירים מספר גדול יותר, מתקבלת תוצאה קטנה יותר.')],
  ['nocalc', () => qNoCalc('5,098 + 3,187', 8285, '5,098 + 2,076', 7174, 'המספר הראשון זהה. ככל שמוסיפים מספר גדול יותר, התוצאה גדולה יותר.')],
  ['nocalc', () => qNoCalc('237 − 149', 88, '237 − 99', 138, 'המספר הראשון זהה. כשמחסירים מספר גדול יותר, מתקבלת תוצאה קטנה יותר.')],
  ['nocalc', () => qNoCalc('459 − 345', 114, '500 − 345', 155, 'מחסירים אותו מספר. ככל שהמספר הראשון גדול יותר, התוצאה גדולה יותר.')],
  ['nocalc', () => qNoCalc('245 + 567', 812, '348 + 600', 948, 'בצד אחד שני המספרים גדולים יותר, ולכן גם הסכום שלו גדול יותר.')],
  ['nocalc', () => qNoCalc('397 + 199', 596, '397 + 678', 1075, 'המספר הראשון זהה. ככל שמוסיפים מספר גדול יותר, התוצאה גדולה יותר.')],
  ['word', () => qWordP('לעמית היו 350 דפים. הוא השתמש ב-149 דפים. כמה דפים נותרו לו?', '350 − 149', 201, 'השתמש אומר שהדפים ירדו, ולכן מחסרים.')],
  ['word', () => qWordP('לטל היו 70 שקלים. הוא קיבל מהוריו עוד 42 שקלים ומאחיו עוד 27 שקלים. כמה שקלים יש לו כעת?', '70 + 42 + 27', 139, 'קיבל עוד אומר שהכסף גדל, ולכן מחברים את כל הסכומים.')],
  ['word', () => qWordP('במאפיית הכפר יש 245 סופגניות. במאפיית השרון יש 16 סופגניות יותר מאשר במאפיית הכפר. כמה סופגניות יש במאפיית השרון?', '245 + 16', 261, 'יותר מאשר... פירושו להוסיף.')],
  ['word', () => qWordP('במאפיית הכפר יש 245 סופגניות, ובמאפיית השרון יש 261 סופגניות. כמה סופגניות יש בשתי המאפיות יחד?', '245 + 261', 506, 'יחד אומר שמחברים את שתי הכמויות.')],
  ['word', () => qWordP('דנה קנתה 5 עפרונות. כל עיפרון עלה לה 7 שקלים. כמה עלו לה כל העפרונות?', '5 × 7', 35, 'מחיר זהה לכל עיפרון: מכפילים את מספר העפרונות במחיר של עיפרון אחד.')],
  ['angleid', () => qAngle(90, 0)],
  ['angleid', () => qAngle(28, 180)],
  ['angleid', () => qAngle(180, 0)],
  ['angleid', () => qAngle(134, 42)],
  ['angleid', () => qAngle(180, 140)],
  ['angleid', () => qAngle(90, 180)],
  ['angleid', () => qAngle(148, 16)],
  ['angleid', qAnglePics],
  ['angledraw', () => sheetDraw('חדה')],
  ['angledraw', () => sheetDraw('קהה')],
  ['angledraw', () => sheetDraw('ישרה')]
].map(([cat, make], i) => ({ id: 's' + (i + 1), cat, make }));
function sheetDraw(target) { angDrawBag = [target]; return genAngleDraw(); }