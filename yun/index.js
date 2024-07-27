function Z(e, t) {
    var n = Object.keys(e);
    if (Object.getOwnPropertySymbols) {
        var r = Object.getOwnPropertySymbols(e);
        t && (r = r.filter((function(t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
        }
        ))),
        n.push.apply(n, r)
    }
    return n
}
function U(e) {
    for (var t = 1; t < arguments.length; t++) {
        var n = null != arguments[t] ? arguments[t] : {};
        t % 2 ? Z(Object(n), !0).forEach((function(t) {
            Object(F.a)(e, t, n[t])
        }
        )) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : Z(Object(n)).forEach((function(t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(n, t))
        }
        ))
    }
    return e
}

  var _ = function(e, t) {
    var n = new G.a.KJUR.crypto.Signature({
        alg: "MD5withRSA"
    })
      , r = G.a.KEYUTIL.getKey(t)
      , o = "";
    for (var a in n.init(r),
    e)
        o += "".concat(a, "=").concat(e[a], "&");
    return o = o.substring(0, o.length - 1),
    n.updateString(o),
    G.a.hextob64(n.sign())
}
  , encrypt = function(e) {
    e = JSON.parse(e);
    var t = {actId: e.actId, openId: e.openId};
    t.nonce = ee(),
    t.timestamp = (new Date).valueOf();
    var n = ""
      , r = function(e, t) {
        var n = [];
        Object.keys(e).forEach((function(e) {
            return n.push(e)
        }
        ));
        var r = t ? n.sort() : n.sort().reverse()
          , o = {};
        for (var a in r)
            o[r[a]] = e[r[a]];
        return o
    }(t, !0);
    for (var o in r)
        n += "".concat(o, "=").concat(r[o], "&");
    return n = n.substring(0, n.length - 1),
    // n = W(H()(n)),
    // {
    //     nonce: t.nonce,
    //     timestamp: t.timestamp,
    //     sign: n
    // }
    {
        timestamp: t.timestamp,
        nonce: t.nonce,
        n
    }
}
  , ee = function() {
    return "xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx".replace(/[xy]/g, (function(e) {
        var t = 16 * Math.random() | 0;
        return ("x" == e ? t : 3 & t | 8).toString(16)
    }
    ))
}
  , te = function(e, t) {
    var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {}
      , r = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : "POST";
    return new Promise((function(o, a) {
        L()({
            url: t,
            data: e,
            method: r,
            headers: n
        }).then((function(e) {
            t == v.c ? (e = e.data).data ? "string" != typeof e.data || -1 == e.data.indexOf('{"') && -1 == e.data.indexOf('["') ? o(e.data.msg) : o(JSON.parse(e.data)) : a(e.msg) : o(e.data)
        }
        )).catch((function(e) {
            a(e)
        }
        ))
    }
    ))
}

function re(e, t) {
    var n = Object.keys(e);
    if (Object.getOwnPropertySymbols) {
        var r = Object.getOwnPropertySymbols(e);
        t && (r = r.filter((function(t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
        }
        ))),
        n.push.apply(n, r)
    }
    return n
}
function oe(e) {
    for (var t = 1; t < arguments.length; t++) {
        var n = null != arguments[t] ? arguments[t] : {};
        t % 2 ? re(Object(n), !0).forEach((function(t) {
            Object(F.a)(e, t, n[t])
        }
        )) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : re(Object(n)).forEach((function(t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(n, t))
        }
        ))
    }
    return e
}