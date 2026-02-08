import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search, SlidersHorizontal } from "lucide-react";
import { TodoFilters as Filters, Priority, Category } from "@/hooks/useTodos";

interface TodoFiltersProps {
  filters: Filters;
  onFiltersChange: (filters: Filters) => void;
  categories: Category[];
}

export function TodoFilters({ filters, onFiltersChange, categories }: TodoFiltersProps) {
  const updateFilter = <K extends keyof Filters>(key: K, value: Filters[K]) => {
    onFiltersChange({ ...filters, [key]: value });
  };

  return (
    <div className="space-y-4 p-4 rounded-xl border border-border bg-card/50">
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <Input
          value={filters.search}
          onChange={(e) => updateFilter("search", e.target.value)}
          placeholder="Search tasks..."
          className="pl-10 bg-input border-border focus:border-primary"
        />
      </div>

      {/* Filter Row */}
      <div className="flex items-center gap-2 flex-wrap">
        <SlidersHorizontal className="w-4 h-4 text-muted-foreground" />
        
        {/* Status Filter */}
        <Select value={filters.status} onValueChange={(v) => updateFilter("status", v as Filters["status"])}>
          <SelectTrigger className="w-[130px] bg-input border-border">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Tasks</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="completed">Completed</SelectItem>
          </SelectContent>
        </Select>

        {/* Priority Filter */}
        <Select value={filters.priority} onValueChange={(v) => updateFilter("priority", v as Priority | "all")}>
          <SelectTrigger className="w-[130px] bg-input border-border">
            <SelectValue placeholder="Priority" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Priorities</SelectItem>
            <SelectItem value="high">🔴 High</SelectItem>
            <SelectItem value="medium">🟡 Medium</SelectItem>
            <SelectItem value="low">🟢 Low</SelectItem>
          </SelectContent>
        </Select>

        {/* Category Filter */}
        <Select value={filters.category} onValueChange={(v) => updateFilter("category", v)}>
          <SelectTrigger className="w-[150px] bg-input border-border">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            {categories.map((cat) => (
              <SelectItem key={cat.id} value={cat.id}>
                <span className="flex items-center gap-2">
                  <span
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: cat.color || "#22C55E" }}
                  />
                  {cat.name}
                </span>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Sort */}
        <Select value={filters.sortBy} onValueChange={(v) => updateFilter("sortBy", v as Filters["sortBy"])}>
          <SelectTrigger className="w-[140px] bg-input border-border">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="created_at">Date Created</SelectItem>
            <SelectItem value="due_date">Due Date</SelectItem>
            <SelectItem value="priority">Priority</SelectItem>
            <SelectItem value="title">Title</SelectItem>
          </SelectContent>
        </Select>

        {/* Sort Order */}
        <Select value={filters.sortOrder} onValueChange={(v) => updateFilter("sortOrder", v as Filters["sortOrder"])}>
          <SelectTrigger className="w-[100px] bg-input border-border">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="desc">Newest</SelectItem>
            <SelectItem value="asc">Oldest</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
