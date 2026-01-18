import { slug } from "github-slugger";
import { marked } from "marked";

// slugify
export const slugify = (content: string) => {
    if (!content) return null;
    return slug(content);
};

// markdownify
export const markdownify = (content: string) => {
    if (!content) return null;
    return marked.parseInline(content);
};

// humanize
export const humanize = (content: string) => {
    if (!content) return null;
    return content
        .replace(/^[\s_]+|[\s_]+$/g, "")
        .replace(/[_\s]+/g, " ")
        .replace(/^[a-z]/, (m) => m.toUpperCase());
};

// plainify
export const plainify = (content: string) => {
    if (!content) return null;
    const parseMarkdown = marked.parse(content);
    const filterBrackets = parseMarkdown.replace(/<\/?[^>]+(>|$)/g, "");
    const filterSpaces = filterBrackets.replace(/[\r\n]\s*[\r\n]/g, "");
    const stripHTML = htmlEntityDecoder(filterSpaces);
    return stripHTML;
};

const htmlEntityDecoder = (htmlWithEntities: string) => {
    let entityList: { [key: string]: string } = {
        "&nbsp;": " ",
        "&lt;": "<",
        "&gt;": ">",
        "&amp;": "&",
        "&quot;": '"',
        "&#39;": "'",
    };
    let htmlWithoutEntities = htmlWithEntities.replace(
        /(&amp;|&lt;|&gt;|&quot;|&#39;)/g,
        (entity) => {
            return entityList[entity];
        }
    );
    return htmlWithoutEntities;
};
