export interface IGroupTag {
  label: string;
  slug: string;
}

// Takes care of the back-end enum values
export const GroupTags = () => {
  const tags: Record<string, IGroupTag> = {
    ACADEMIC: {
      label: 'Acadêmico',
      slug: 'academic',
    },
    PERSONAL: {
      label: 'Pessoal',
      slug: 'personal',
    },
    PROFESSIONAL: {
      label: 'Profissional',
      slug: 'professional',
    },
    UNDEFINED: {
      label: 'Outro',
      slug: 'undefined',
    },
  };

  const api = {
    defaultTag: (): IGroupTag => tags.UNDEFINED,
    // To be used in the select components
    labels: (): string[] => Object.values(tags).map((tag) => tag.label),
    // To be passed in the payload to the back-end
    slugs: (): string[] => Object.values(tags).map((tag) => tag.slug),
    slugByLabel: (value: string): string => {
      const filtered = Object.values(tags).filter((tag) => tag.label === value.trim());
      return filtered.length > 0 ? filtered[0].slug : tags.UNDEFINED.slug;
    },
    labelBySlug: (value: string): string => {
      const filtered = Object.values(tags).filter((tag) => tag.slug === value.trim());
      return filtered.length > 0 ? filtered[0].label : tags.UNDEFINED.label;
    },
  };

  return api;
};
