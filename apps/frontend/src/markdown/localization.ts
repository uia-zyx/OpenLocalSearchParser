export function localizeMarkdownPageHeadings(markdown: string, pageLabel: string): string {
  return markdown.replace(
    /(^|\n)(\s{0,3}#{1,6}\s+)Page\s+(\d+)\b/g,
    (_match, lineStart: string, headingPrefix: string, pageNumber: string) =>
      `${lineStart}${headingPrefix}${pageLabel} ${pageNumber}`,
  );
}
