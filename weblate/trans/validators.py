# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2019 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from weblate.checks import CHECKS
from weblate.trans.util import parse_flags

EXTRA_FLAGS = {
    v.enable_string: v.name
    for k, v in CHECKS.items()
    if v.default_disabled and not v.param_type
}
TYPED_FLAGS = {
    v.enable_string: v.param_type
    for k, v in CHECKS.items()
    if v.param_type
}

EXTRA_FLAGS['rst-text'] = ugettext_lazy('RST text')
EXTRA_FLAGS['md-text'] = ugettext_lazy('Markdown text')
EXTRA_FLAGS['xml-text'] = ugettext_lazy('XML text')
EXTRA_FLAGS['dos-eol'] = ugettext_lazy('DOS line endings')
EXTRA_FLAGS['url'] = ugettext_lazy('URL')
EXTRA_FLAGS['auto-java-messageformat'] = ugettext_lazy(
    'Automatically detect Java MessageFormat'
)

IGNORE_CHECK_FLAGS = {CHECKS[x].ignore_string for x in CHECKS}


def validate_filemask(val):
    """Validate that filemask contains *."""
    if '*' not in val:
        raise ValidationError(
            _('Filemask does not contain * as a language placeholder!')
        )


def validate_autoaccept(val):
    """Validate correct value for autoaccept."""
    if val == 1:
        raise ValidationError(_(
            'A value of 1 is not allowed for autoaccept as '
            'it would permit users to vote on their own suggestions.'
        ))


def validate_check_flags(val):
    """Validate check influencing flags."""
    for flag in parse_flags(val):
        if ':' in flag:
            key, value = flag.split(':', 1)
            if key in TYPED_FLAGS:
                try:
                    TYPED_FLAGS[key](value)
                    continue
                except Exception:
                    raise ValidationError(_('Invalid translation flag: "%s"') % flag)
        elif flag in EXTRA_FLAGS or flag in IGNORE_CHECK_FLAGS:
            continue
        raise ValidationError(_('Invalid translation flag: "%s"') % flag)
