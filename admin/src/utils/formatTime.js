import normalizeNumber from '@/utils/normalizeNumber'

export default function formatTime(dataString) {
    let date = new Date(dataString);
    let year = date.getFullYear();
    let month = normalizeNumber(date.getMonth()+1);
    let day = normalizeNumber(date.getDate());
    let minutes = normalizeNumber(date.getMinutes());
    let hours = normalizeNumber(date.getHours());
    let seconds = normalizeNumber(date.getSeconds());

    return `${day}.${month}.${year}   ${hours}:${minutes}:${seconds}`
}
