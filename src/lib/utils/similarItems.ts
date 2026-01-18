const similerItems = (currentItem: any, allItems: any[], slug: string) => {
    let categories: string[] = [];
    let tags: string[] = [];

    // set categories
    if (currentItem.data.categories && currentItem.data.categories.length > 0) {
        categories = currentItem.data.categories;
    }

    // set tags
    if (currentItem.data.tags && currentItem.data.tags.length > 0) {
        tags = currentItem.data.tags;
    }

    // filter by categories
    const filterByCategories = allItems.filter((item: any) =>
        categories.find((category) => item.data.categories?.includes(category))
    );

    // filter by tags
    const filterByTags = allItems.filter((item: any) =>
        tags.find((tag) => item.data.tags?.includes(tag))
    );

    // merged items
    const mergedItems = [...new Set([...filterByCategories, ...filterByTags])];

    // filter by slug
    const filterBySlug = mergedItems.filter((product) => product.slug !== slug);

    return filterBySlug;
};

export default similerItems;
