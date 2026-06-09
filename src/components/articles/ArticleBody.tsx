import { cn } from "@/lib/utils";

interface ArticleBodyProps {
  body: string;
  className?: string;
}

function parseBold(text: string): React.ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) =>
    part.startsWith("**") && part.endsWith("**") ? (
      <strong key={i}>{part.slice(2, -2)}</strong>
    ) : (
      part
    )
  );
}

function parseTableRow(line: string): string[] {
  return line
    .split("|")
    .filter((_, i, arr) => i > 0 && i < arr.length - 1)
    .map((cell) => cell.trim());
}

function isSeparatorRow(line: string): boolean {
  return /^\|[\s|-]+\|/.test(line);
}

export default function ArticleBody({ body, className }: ArticleBodyProps) {
  const lines = body.split("\n");
  const elements: React.ReactNode[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // h1
    if (line.startsWith("# ")) {
      elements.push(
        <h1 key={i} className="text-2xl font-black text-zinc-900 dark:text-zinc-100 mt-6 mb-3 first:mt-0">
          {parseBold(line.slice(2))}
        </h1>
      );
      i++;
      continue;
    }

    // h2
    if (line.startsWith("## ")) {
      elements.push(
        <h2 key={i} className="text-lg font-bold text-zinc-900 dark:text-zinc-100 mt-6 mb-2 pb-1 border-b border-zinc-100 dark:border-zinc-800">
          {parseBold(line.slice(3))}
        </h2>
      );
      i++;
      continue;
    }

    // h3
    if (line.startsWith("### ")) {
      elements.push(
        <h3 key={i} className="text-base font-bold text-zinc-800 dark:text-zinc-200 mt-4 mb-2">
          {parseBold(line.slice(4))}
        </h3>
      );
      i++;
      continue;
    }

    // Table: collect consecutive table lines
    if (line.startsWith("|")) {
      const tableLines: string[] = [];
      while (i < lines.length && lines[i].startsWith("|")) {
        tableLines.push(lines[i]);
        i++;
      }
      const nonSep = tableLines.filter((l) => !isSeparatorRow(l));
      if (nonSep.length >= 2) {
        const headers = parseTableRow(nonSep[0]);
        const rows = nonSep.slice(1);
        elements.push(
          <div key={`table-${i}`} className="table-scroll my-4 rounded-lg border border-zinc-200 dark:border-zinc-800 overflow-hidden">
            <table className="w-full text-sm min-w-max">
              <thead className="bg-zinc-50 dark:bg-zinc-800/50">
                <tr>
                  {headers.map((h, hi) => (
                    <th key={hi} className="px-4 py-2.5 text-left text-xs font-semibold text-zinc-600 dark:text-zinc-300">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
                {rows.map((row, ri) => (
                  <tr key={ri} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/30">
                    {parseTableRow(row).map((cell, ci) => (
                      <td key={ci} className="px-4 py-2.5 text-zinc-700 dark:text-zinc-300">
                        {parseBold(cell)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      }
      continue;
    }

    // Empty line → paragraph break
    if (line.trim() === "") {
      i++;
      continue;
    }

    // Regular paragraph
    elements.push(
      <p key={i} className="text-zinc-700 dark:text-zinc-300 leading-relaxed mb-3 text-[15px]">
        {parseBold(line)}
      </p>
    );
    i++;
  }

  return (
    <div className={cn("prose-like", className)}>
      {elements}
    </div>
  );
}
