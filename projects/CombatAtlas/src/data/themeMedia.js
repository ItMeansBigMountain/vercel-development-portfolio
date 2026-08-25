const CLEAN_THEME = 'clean-icons';
const PHOTO_THEME = 'real-photography';

export const visualThemes = [
  {
    id: CLEAN_THEME,
    label: 'Clean Icons',
    shortLabel: 'Icons',
    description: 'Fast, offline geometric illustrations that preserve the original clean CombatAtlas look.',
  },
  {
    id: PHOTO_THEME,
    label: 'Real Martial Arts Photography',
    shortLabel: 'Photos',
    description: 'Licensed Wikimedia Commons photography with responsive crops and attribution metadata.',
  },
];

const commonsPhotos = {
  boxing: photo('A boxing school established in Llanarmon by W G Buchanan, an ex-air force boxing champion, and the Rev T D Williams (15162039803).jpg', 'Boxers practicing in a historic Welsh boxing school', 'CC0', 'Geoff Charles', 'National Library of Wales / Flickr via Wikimedia Commons'),
  kickboxing: photo('Adidas Kickboxing equipment used by Hamid Amni.jpg', 'Kickboxing gloves and protective training equipment', 'CC BY-SA 4.0', 'Pegah hadad', 'Own work via Wikimedia Commons'),
  'muay-thai': photo('Muay-Thai Thai-boxing-kids IMG 1824.jpg', 'Muay Thai trainees practicing in a boxing ring', 'CC BY-SA 4.0', 'Per Meistrup', 'Own work via Wikimedia Commons'),
  karate: photo('2026-05-24 61. Karate-Europameisterschaften 2026 Frankfurt-Main STP 6787.jpg', 'Karate athletes competing on a tatami mat', 'CC BY-SA 4.0', 'Steffen Prößdorf', 'Self-photographed via Wikimedia Commons'),
  taekwondo: photo('WTF Taekwondo 1.jpg', 'Taekwondo athletes sparring with protective gear and high kicks', 'CC BY-SA 3.0', 'Stefan Pettersson', 'Own work via Wikimedia Commons'),
  'kung-fu': photo('Kung Fu Tournament.jpg', 'Kung Fu tournament athlete performing in uniform', 'CC BY-SA 4.0', 'ShorelineTaiji', 'Own work via Wikimedia Commons'),
  sanda: photo('Sanshou (San da) - kick (practice fight) Katwijk, dec 4, 2006.JPG', 'Sanda athletes practicing a kick during a sanshou bout', 'CC BY-SA 3.0', 'Richardkw', 'Own work via Wikimedia Commons'),
  judo: photo('EIJC 2025 Kata - 54381747372.jpg', 'Judo practitioners demonstrating kata grips', 'Public domain', 'Edmonton International Judo Championship', 'Flickr via Wikimedia Commons'),
  bjj: photo('BJJ, brazilian-jiujitsu 01.jpg', 'Brazilian Jiu-Jitsu athletes grappling on mats', 'CC BY-SA 4.0', 'Yossigur', 'Own work via Wikimedia Commons'),
  wrestling: photo('Amateur Wrestling Brothers 2017-06-09.jpg', 'Amateur wrestlers hand fighting on a mat', 'CC BY-SA 4.0', 'Baynosuke', 'Own work via Wikimedia Commons'),
  hapkido: photo('Hapkido takmicenje.jpg', 'Hapkido athletes sparring in sport competition', 'CC BY-SA 4.0', 'Aster Igor', 'Own work via Wikimedia Commons'),
  fencing: photo('Fencing in Greece. Fencing training at Athenaikos Fencing Club with fencers from other clubs.jpg', 'Fencers training at a fencing club', 'CC BY-SA 4.0', 'George E. Koronaios', 'Own work via Wikimedia Commons'),
  kendo: photo('Georgia Kendo Tournament 2025.jpg', 'Kendo athletes facing each other at the start of a match', 'CC BY 4.0', 'Huntsmanleader', 'Own work via Wikimedia Commons'),
  'arnis-kali-eskrima': photo('Eskrima.jpg', 'Eskrima practitioners stick fighting during Filipino martial arts training', 'CC BY 3.0', 'Mr.Colling', 'Own work via Wikimedia Commons'),
  hema: photo('Tarr Bence László, HEMA - Historical European Martial Arts.jpg', 'Historical European Martial Arts practitioner with longsword equipment', 'CC BY-SA 4.0', 'Cyberguru', 'Own work via Wikimedia Commons'),
  capoeira: photo('Roda de Capoeira Angola.jpg', 'Capoeira practitioners playing in a roda', 'CC BY-SA 4.0', 'Ayres Alves de Lima Sales', 'Own work via Wikimedia Commons'),
  silat: photo('Pencak Silat Betawi 2.jpg', 'Pencak Silat Betawi practitioner demonstrating a traditional stance', 'CC BY-SA 4.0', 'Gunawan Kartapranata', 'Own work via Wikimedia Commons'),
};

function photo(fileName, alt, license, creator, credit) {
  const encoded = encodeURIComponent(fileName).replace(/%2F/g, '/');
  const filePage = `https://commons.wikimedia.org/wiki/File:${encoded}`;
  return {
    fileName,
    imageUrl: `https://commons.wikimedia.org/wiki/Special:FilePath/${encoded}?width=960`,
    srcSet: [480, 720, 960].map((width) => `https://commons.wikimedia.org/wiki/Special:FilePath/${encoded}?width=${width} ${width}w`).join(', '),
    imageAlt: alt,
    sourceUrl: filePage,
    license,
    creator,
    credit,
  };
}

function cleanIconMedia(art) {
  return {
    imageUrl: art.imageUrl,
    imageAlt: art.imageAlt,
    sourceUrl: null,
    license: 'Generated inline SVG illustration',
    creator: 'CombatAtlas',
    credit: 'Generated locally from app data; no external image request.',
  };
}

function findPhotoForArt(art) {
  return commonsPhotos[art.id] || cleanIconMedia(art);
}

export function prefersReducedData() {
  return Boolean(globalThis.navigator?.connection?.saveData);
}

export function normalizeVisualTheme(themeId) {
  if (prefersReducedData()) return CLEAN_THEME;
  return visualThemes.some((theme) => theme.id === themeId) ? themeId : CLEAN_THEME;
}

export function getArtMedia(art, themeId = CLEAN_THEME) {
  if (normalizeVisualTheme(themeId) !== PHOTO_THEME) {
    return cleanIconMedia(art);
  }
  return findPhotoForArt(art);
}

export function getDrillThemeMedia(drill, art, themeId = CLEAN_THEME, cleanMedia) {
  if (normalizeVisualTheme(themeId) !== PHOTO_THEME) return cleanMedia;
  const photoMedia = findPhotoForArt(art);
  return {
    ...photoMedia,
    imageAlt: `${art.name} training photo representing ${drill.title}`,
    youtubeUrl: cleanMedia.youtubeUrl,
  };
}

export function mediaAttribution(media) {
  if (!media?.sourceUrl) return media?.credit || 'Generated locally by CombatAtlas.';
  return `${media.license} · ${media.creator} · ${media.sourceUrl}`;
}
