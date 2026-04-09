```markdown
---
name: ui
description: npx shadcn・components.json・cn()ユーティリティ・CSS変数テーマ（--background/--primary等）・Radix UIプリミティブを使ったReact/Next.jsのUI実装が発生したら必ずこのスキルを使え。Button・Dialog・DataTable・Form・Sidebar・Command等のshadcn/uiコンポーネント追加・カスタマイズ・レジストリ構築にも即座に参照せよ。
---

# ui

## 概要
shadcn/uiはTailwind CSS v4ベースの50以上のReactコンポーネントをソースコードとしてプロジェクトにコピーする「Copy-Owned」モデルのUIライブラリである。Radix UIプリミティブ上に構築され、CLIによるコンポーネント追加・CSS変数によるテーマカスタマイズ・カスタムレジストリ公開をサポートする。パッケージ依存ではなくコード所有のため、自由にカスタマイズできる。

## いつ使うか
- `npx shadcn@latest add` でコンポーネント（Button・Dialog・Table・Form・Sidebar等）を追加したい
- `components.json` の設定やパスエイリアスを変更・トラブルシュートしたい
- CSS変数（`--background`・`--primary`・`--radius`等）でテーマをカスタマイズしたい
- `cn()` ユーティリティでクラス名を条件付きマージしたい
- react-hook-form + zod + shadcn/ui Formで型安全なフォームを構築したい
- DataTable（TanStack Table統合）でソート・フィルタ・ページネーション付きテーブルを実装したい
- カスタムコンポーネントレジストリをJSON形式で定義・公開したい

## 主要コマンド・API

### CLIによる初期化・コンポーネント追加
```bash
# 初期化（Tailwind v4対応、components.jsonを生成）
npx shadcn@latest init

# 単一コンポーネントを追加
npx shadcn@latest add button

# 複数コンポーネントを一括追加
npx shadcn@latest add dialog table form select

# 差分確認（アップストリームの更新をチェック）
npx shadcn@latest diff

# 外部レジストリURLから追加
npx shadcn@latest add https://example.com/r/styles/default/my-component.json
```

### cn()ユーティリティ（クラスマージ）
```typescript
// lib/utils.ts — shadcn init で自動生成される
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// 使用例：条件付きクラスの安全なマージ
<Button className={cn("w-full", isLoading && "opacity-50 cursor-not-allowed")}>
  送信
</Button>
```

### CSS変数によるテーマ定義（Tailwind v4）
```css
/* app/globals.css */
@import "tailwindcss";

@layer base {
  :root {
    --background: oklch(1 0 0);
    --foreground: oklch(0.145 0 0);
    --primary: oklch(0.205 0 0);
    --primary-foreground: oklch(0.985 0 0);
    --secondary: oklch(0.97 0 0);
    --muted: oklch(0.97 0 0);
    --accent: oklch(0.97 0 0);
    --destructive: oklch(0.577 0.245 27.325);
    --border: oklch(0.922 0 0);
    --ring: oklch(0.708 0 0);
    --radius: 0.625rem;
  }

  .dark {
    --background: oklch(0.145 0 0);
    --foreground: oklch(0.985 0 0);
    --primary: oklch(0.985 0 0);
  }
}
```

### Formコンポーネント（react-hook-form + zod統合）
```tsx
"use client"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({ name: z.string().min(1, "必須") })

export function MyForm() {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { name: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit((data) => console.log(data))}>
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>名前</FormLabel>
              <FormControl><Input {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">送信</Button>
      </form>
    </Form>
  )
}
```

### DataTable（TanStack Table統合）
```tsx
"use client"
import { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"

// 1. カラム定義
const columns: ColumnDef<Payment>[] = [
  { accessorKey: "status", header: "ステータス" },
  { accessorKey: "amount", header: "金額",
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue("amount"))
      return new Intl.NumberFormat("ja-JP", { style: "currency", currency: "JPY" }).format(amount)
    },
  },
]

// 2. DataTableコンポーネントで使用
<DataTable columns={columns} data={payments} />
```

### カスタムレジストリJSON定義
```json
{
  "name": "my-component",
  "type": "registry:ui",
  "dependencies": ["@radix-ui/react-dialog"],
  "files": [
    {
      "path": "components/ui/my-component.tsx",
      "content": "import * as React from \"react\"\nimport * as DialogPrimitive from \"@radix-ui/react-dialog\"\nimport { cn } from \"@/lib/utils\"\n\nconst MyComponent = React.forwardRef<...>(...)\n\nexport { MyComponent }",
      "type": "registry:ui"
    }
  ],
  "cssVars": {
    "light": { "--my-color": "oklch(0.5 0.2 250)" },
    "dark":  { "--my-color": "oklch(0.7 0.2 250)" }
  }
}
```

## ワークフロー例

### 典型例①：新規Next.jsプロジェクトへのshadcn/ui導入
1. `npx shadcn@latest init` を実行 → `components.json` が生成される
2. `components.json` の `aliases.components`（デフォルト: `@/components/ui`）と `tsconfig.json` のパスエイリアスが一致していることを確認
3. `npx shadcn@latest add button card input` で必要なコンポーネントを追加
4. `app/globals.css` のCSS変数を編集しブランドカラーに合わせる
5. `import { Button } from "@/components/ui/button"` でローカルパスからimport

### 典型例②：型安全なフォーム構築
1. `npx shadcn@latest add form input select` でフォーム関連コンポーネントを追加
2. `npm install @hookform/resolvers zod` を追加（shadcn CLIが自動で入れない場合）
3. zodスキーマを定義し、`useForm` + `zodResolver` でバリデーションを接続
4. `FormField` > `FormItem` > `FormLabel` + `FormControl` + `FormMessage` の階層でUIを構築
5. `form.handleSubmit` でsubmit処理を実装

### 典型例③：テーマカスタマイザーからのデザイン適用
1. `https://ui.shadcn.com/themes` でカラー・ラジウスをインタラクティブに調整
2. 「Copy code」でCSS変数定義をコピー
3. `app/globals.css` の `:root` と `.dark` に貼り付け
4. `npx shadcn@latest diff` で既存コンポーネントに変更が必要か確認

### 典型例④：カスタムレジストリの公開
1. `public/r/styles/default/` にコンポーネントのJSONファイルを配置
2. `name`・`type`・`files`・`dependencies`・`cssVars` をスキーマに従い定義
3. デプロイ後、`npx shadcn@latest add https://your-domain.com/r/styles/default/my-component.json` でインストール可能

## 注意点
- **`"use client"` が必須のコンポーネント**: Dialog・DropdownMenu・Form・Tabs・Toast等のインタラクティブコンポーネントはClient Componentでなければ動作しない。Server Componentから直接使うと `useState is not a function` エラーになる
- **`cn()` を使わずにclassNameを直接結合しない**: `className={"px-4 " + props.className}` ではTailwindクラスが競合する。必ず `cn("px-4", props.className)` を使うこと。`cn` は `tailwind-merge` で競合するユーティリティクラスを正しく解決する
- **Copy-Ownedモデルのアップデート**: `npx shadcn@latest diff` で上流との差分を確認してから手動マージ。`add` を再実行すると既存のカスタマイズが上書きされる
- **Tailwind v4専用**: CSS変数はoklch記法。v3プロジェクト（`tailwind.config.js` + hsl記法）とは互換性がない。v3からの移行は `@tailwindcss/upgrade` を先に実行
- **`components.json` のパスエイリアス不一致**: `aliases.components` が `tsconfig.json` の `paths` と一致しないとCLIが間違った場所にファイルを配置する。monorepoでは特に注意
- **Form + zodの依存関係**: `npx shadcn@latest add form` は `react-hook-form` と `@hookform/resolvers` を `dependencies` に記載するが自動インストールされない場合がある。`npm install` が必要
- **DataTableは複合コンポーネント**: shadcn CLIには `data-table` という単一コンポーネントはない。公式ドキュメントの手順に従い `table` コンポーネント + `@tanstack/react-table` を組み合わせて手動構築する
- **ダークモード切替**: `next-themes` の `ThemeProvider` で `attribute="class"` を指定すること。`attribute="data-theme"` だとshadcn/uiのCSS変数セレクタ（`.dark`）が効かない

## 関連スキル
- **Next.js**: App Router・Server Components・`"use client"` ディレクティブの使い分け
- **Tailwind CSS**: v4のCSS変数・oklch色空間・`@layer base` の理解が前提
- **Radix UI**: shadcn/uiの基盤プリミティブ。アクセシビリティ・キーボードナビゲーション実装
- **react-hook-form + zod**: Formコンポーネントのバリデーション基盤
- **TanStack Table**: DataTableのソート・フィルタ・ページネーション実装
```
