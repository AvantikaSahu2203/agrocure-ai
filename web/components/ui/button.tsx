import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

// Needs: npm install class-variance-authority @radix-ui/react-slot
// I should install these too. Ideally.
// But for now I'll implement a simpler version without cva/slot if I can't install more deps easily.
// Actually, I can just use simple props without cva for MVP to avoid extra deps if problematic.
// But cva is standard for shadcn.
// I'll assume I can install them. Or just use a simpler implementation.
// Let's use simpler implementation for now to reduce complexity and deps.

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive' | 'link';
    size?: 'sm' | 'md' | 'lg';
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = 'primary', size = 'md', ...props }, ref) => {

        const baseStyles = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"

        const variants = {
            primary: "bg-green-600 text-white shadow hover:bg-green-700",
            secondary: "bg-slate-100 text-slate-900 shadow-sm hover:bg-slate-200",
            outline: "border border-input bg-transparent shadow-sm hover:bg-accent hover:text-accent-foreground",
            ghost: "hover:bg-slate-100 hover:text-slate-900",
            destructive: "bg-red-500 text-white shadow-sm hover:bg-red-600",
            link: "text-primary underline-offset-4 hover:underline",
        }

        const sizes = {
            sm: "h-8 px-3 text-xs",
            md: "h-9 px-4 py-2",
            lg: "h-10 px-8",
        }

        return (
            <button
                className={cn(baseStyles, variants[variant], sizes[size], className)}
                ref={ref}
                {...props}
            />
        )
    }
)
Button.displayName = "Button"

export { Button }
