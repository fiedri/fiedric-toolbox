function domainName(url) {
    return url.replace(/(https?:\/\/)?(www\.)?/, '').split('.')[0];
}

console.log(domainName("www.xakep.ru"));