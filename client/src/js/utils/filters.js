function priceFilter(value, prefix) {
    if (prefix === undefined) {
        prefix = 'За '
    }
    if (value !== null) {
      if (value > 0) {
        return `${prefix}<span class="price">${value}</span>`;
      } else {
        return "Бесплатно";
      }
    } else {
      return "";
    }
}

function timeFilter(from_time, to_time) {
    if (from_time || to_time) {
      if (from_time != to_time) {
        from_time = from_time ? `от ${from_time}` : "";
        to_time = to_time ? ` до ${to_time}` : "";
        return `${from_time}${to_time} дней`;
      } else {
        if (from_time == 1) {
          return `от 1 дня`;
        } else {
          return `от ${from_time} дней`;
        }
      }
    } else {
      return "";
    }
}

export { priceFilter,  timeFilter };