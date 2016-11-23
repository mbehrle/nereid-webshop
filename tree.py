# -*- coding: utf-8 -*-
from trytond.pool import PoolMeta
from trytond.model import fields

from nereid import Markup

__all__ = ['Node']
__metaclass__ = PoolMeta


class Node:
    __name__ = "product.tree_node"

    product_as_menu_children = fields.Boolean('Product as menu children?')

    def get_menu_item(self, max_depth):
        """
        Return dictionary with serialized node for menu item
        {
            title: <display name>,
            link: <url>,
            record: <instance of record> # if type_ is `record`
        }
        """
        res = {
            'record': self,
            'title': self.name,
            'link': self.get_absolute_url(),
            'image': self.image,
        }
        if max_depth > 0:
            res['children'] = self.get_children(max_depth=max_depth - 1)

        return res

    def get_children(self, max_depth):
        """
        Return serialized menu_item for current treenode
        """
        if self.product_as_menu_children:
            return [
                child.get_menu_item(max_depth=max_depth - 1)
                for child in self.get_products()
            ]
        else:
            return [
                child.get_menu_item(max_depth=max_depth - 1)
                for child in self.children
            ]

    def get_meta_description(self):
        '''
        Provide a useful description for the meta description tag
        https://support.google.com/webmasters/answer/79812?hl=en&ref_topic=4617741
        https://support.google.com/webmasters/answer/35624?rd=1#1
            <meta name="Description" CONTENT="Author: A.N. Author,
            Illustrator: P. Picture, Category: Books, Price:  £9.24,
            Length: 784 pages">
        '''
        description = 'Category: %s' % self.rec_name
        if self.products:
            description += ', Products: ' + '; '.join(
                [p.product.name for p in self.products])
        elif self.children:
            description += ', Content: ' + '; '.join(
                [p.name for p in self.children])
        return Markup(description)
