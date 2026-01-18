export const sortByDate = (array: any[]) => {
    const sortedArray = array.sort(
        (a: any, b: any) =>
            new Date(b.data.date && b.data.date).valueOf() -
            new Date(a.data.date && a.data.date).valueOf()
    );
    return sortedArray;
};

export const sortByWeight = (array: any[]) => {
    const sortedArray = array.sort(
        (a: any, b: any) =>
            (a.data.weight ? a.data.weight : 100) -
            (b.data.weight ? b.data.weight : 100)
    );
    return sortedArray;
};
