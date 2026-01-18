const readingTime = (content: string): string => {
    const wordsPerMinute = 200;
    const numberOfWords = content.split(/\s/g).length;
    const minutes = numberOfWords / wordsPerMinute;
    const readTime = Math.ceil(minutes);
    return `${readTime} Min read`;
};

export default readingTime;
