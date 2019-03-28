from digg_paginator import DiggPaginator


class DiggPaginatorViewMixin(object):

    paginator_class = DiggPaginator
    paginate_by = 12

    paginate_orphans = 0
    paginate_allow_empty_first_page = True
    paginate_body = 5
    paginate_padding = 2
    paginate_margin = 2
    paginate_tail = 1

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        return(super(DiggPaginatorViewMixin, self).get_paginator(
               queryset,
               per_page,
               orphans=self.paginate_orphans,
               allow_empty_first_page=self.paginate_allow_empty_first_page,
               body=self.paginate_body,
               padding=self.paginate_padding,
               margin=self.paginate_margin,
               tail=self.paginate_tail,
               **kwargs)
               )
